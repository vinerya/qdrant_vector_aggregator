import os
from .utils import load_qdrant_collection, save_qdrant_collection, load_metadata, save_metadata
from .embedding_methods import calculate_embedding
from .qdrant_collection_helpers import create_qdrant_points, get_vector_dimension
from .config import QDRANT_URL, QDRANT_API_KEY
from qdrant_client.models import Distance

def aggregate_embeddings(
    input_collection_name,
    column_name,
    output_collection_name,
    method="average",
    weights=None,
    trim_percentage=0.1,
    qdrant_url=None,
    api_key=None,
    distance_metric=Distance.COSINE,
    metadata_path=None,
    output_metadata_path=None
):
    """
    Aggregate embeddings from a Qdrant collection based on a metadata column.

    Parameters:
        input_collection_name (str): Name of the input Qdrant collection
        column_name (str): Metadata field by which to aggregate embeddings
        output_collection_name (str): Name of the output Qdrant collection
        method (str): Aggregation method (default: "average")
        weights (list, optional): Weights for weighted_average method
        trim_percentage (float): Fraction to trim for trimmed_mean (default: 0.1)
        qdrant_url (str, optional): URL of Qdrant server (default: from .env or "http://localhost:6333")
        api_key (str, optional): API key for Qdrant Cloud (default: from .env)
        distance_metric (Distance): Distance metric for the output collection (default: COSINE)
        metadata_path (str, optional): Path to load additional metadata
        output_metadata_path (str, optional): Path to save aggregated metadata

    Returns:
        tuple: (output_collection_name, output_metadata_path)
    """
    # Use environment variables if not provided
    if qdrant_url is None:
        qdrant_url = QDRANT_URL
    if api_key is None:
        api_key = QDRANT_API_KEY

    # Load Qdrant client
    client = load_qdrant_collection(input_collection_name, qdrant_url, api_key)

    # Collect embeddings by column value
    embeddings_by_column, metadata_by_column = _collect_embeddings_by_column(
        client, input_collection_name, column_name
    )

    # Calculate representative embeddings
    representative_embeddings = {}
    for column_value, embeddings in embeddings_by_column.items():
        representative_embeddings[column_value] = calculate_embedding(
            embeddings, method, weights, trim_percentage
        )

    # Create Qdrant points
    points = create_qdrant_points(representative_embeddings, metadata_by_column)
    vector_size = get_vector_dimension(representative_embeddings)

    # Save to new collection
    save_qdrant_collection(
        client, output_collection_name, points, vector_size, distance_metric
    )

    # Save metadata if path provided
    if output_metadata_path:
        save_metadata(metadata_by_column, output_metadata_path)

    return output_collection_name, output_metadata_path

def _collect_embeddings_by_column(client, collection_name, column_name):
    """
    Collect embeddings from Qdrant collection grouped by a metadata column.
    Also collects chunks with their metadata for smart content concatenation.

    Parameters:
        client (QdrantClient): Qdrant client instance
        collection_name (str): Name of the collection
        column_name (str): Metadata field to group by

    Returns:
        tuple: (embeddings_by_column, metadata_by_column, chunks_by_column)
    """
    embeddings_by_column = {}
    chunks_by_column = {}  # Store all chunks with their metadata

    # Scroll through all points in the collection
    offset = None
    limit = 100  # Batch size

    while True:
        # Retrieve points
        points, next_offset = client.scroll(
            collection_name=collection_name,
            limit=limit,
            offset=offset,
            with_payload=True,
            with_vectors=True
        )

        if not points:
            break

        # Process each point
        for point in points:
            payload = point.payload
            vector = point.vector

            # Handle nested metadata fields (e.g., "metadata.name")
            column_value = None
            if payload:
                if '.' in column_name:
                    # Handle nested fields like "metadata.name"
                    parts = column_name.split('.')
                    temp = payload
                    for part in parts:
                        if isinstance(temp, dict) and part in temp:
                            temp = temp[part]
                        else:
                            temp = None
                            break
                    column_value = temp
                elif column_name in payload:
                    # Direct field access
                    column_value = payload[column_name]

            if column_value is not None:
                if column_value not in embeddings_by_column:
                    embeddings_by_column[column_value] = []
                    chunks_by_column[column_value] = []

                embeddings_by_column[column_value].append(vector)
                chunks_by_column[column_value].append(payload)

        # Check if there are more points
        if next_offset is None:
            break
        offset = next_offset

    # Convert lists to numpy arrays
    import numpy as np
    for column_value in embeddings_by_column:
        embeddings_by_column[column_value] = np.array(embeddings_by_column[column_value])

    # Create aggregated metadata with smart content handling
    metadata_by_column = _create_aggregated_metadata(chunks_by_column)

    return embeddings_by_column, metadata_by_column

def _create_aggregated_metadata(chunks_by_column):
    """
    Create aggregated metadata with smart page_content concatenation.
    Detects ordering fields and concatenates content if possible.

    Parameters:
        chunks_by_column (dict): Dictionary mapping column values to lists of chunk payloads

    Returns:
        dict: Dictionary mapping column values to aggregated metadata
    """
    metadata_by_column = {}

    # Possible ordering field names to check
    ordering_fields = [
        'chunk_index', 'chunk_number', 'chunk_id', 'chunk',
        'page', 'page_number', 'page_num',
        'sequence', 'seq', 'order', 'index', 'position',
        'id'  # Check id last as it might not be sequential
    ]

    for column_value, chunks in chunks_by_column.items():
        # Start with the first chunk's metadata as base
        aggregated_meta = chunks[0].copy() if chunks else {}

        # Add chunk statistics
        aggregated_meta['chunk_count'] = len(chunks)

        # Try to find ordering field
        ordering_field = None
        for field in ordering_fields:
            # Check in top-level metadata
            if field in chunks[0]:
                ordering_field = field
                break
            # Check in nested metadata
            if 'metadata' in chunks[0] and isinstance(chunks[0]['metadata'], dict):
                if field in chunks[0]['metadata']:
                    ordering_field = ('metadata', field)
                    break

        # Handle page_content concatenation
        if ordering_field and 'page_content' in chunks[0]:
            try:
                # Extract ordering values and sort chunks
                chunks_with_order = []
                for chunk in chunks:
                    if isinstance(ordering_field, tuple):
                        # Nested field
                        order_val = chunk.get(ordering_field[0], {}).get(ordering_field[1])
                    else:
                        # Top-level field
                        order_val = chunk.get(ordering_field)

                    if order_val is not None:
                        chunks_with_order.append((order_val, chunk))

                # Sort by ordering value
                chunks_with_order.sort(key=lambda x: x[0])

                # Concatenate page_content in order
                concatenated_content = []
                for _, chunk in chunks_with_order:
                    content = chunk.get('page_content', '')
                    if content:
                        concatenated_content.append(content)

                aggregated_meta['page_content'] = '\n\n'.join(concatenated_content)
                aggregated_meta['has_ordered_content'] = True
                aggregated_meta['ordering_field'] = ordering_field if isinstance(ordering_field, str) else '.'.join(ordering_field)

            except Exception as e:
                # If sorting fails, set empty content
                aggregated_meta['page_content'] = ''
                aggregated_meta['has_ordered_content'] = False
                aggregated_meta['ordering_error'] = str(e)
        else:
            # No ordering field found, set empty content
            aggregated_meta['page_content'] = ''
            aggregated_meta['has_ordered_content'] = False

        metadata_by_column[column_value] = aggregated_meta

    return metadata_by_column
