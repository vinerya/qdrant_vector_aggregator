from qdrant_client.models import PointStruct
import numpy as np
import uuid

def create_qdrant_points(representative_embeddings, metadata_by_column):
    """
    Create Qdrant points from representative embeddings and metadata.

    Parameters:
        representative_embeddings (dict): Dictionary mapping column values to embeddings
        metadata_by_column (dict): Dictionary mapping column values to metadata

    Returns:
        list: List of PointStruct objects ready for Qdrant upload
    """
    points = []

    for idx, (column_value, embedding) in enumerate(representative_embeddings.items()):
        # Get the metadata from metadata_by_column
        meta = metadata_by_column.get(column_value, {'id': column_value})

        # Create a unique ID for the point
        point_id = str(uuid.uuid4())

        # Create PointStruct
        point = PointStruct(
            id=point_id,
            vector=embedding.tolist(),
            payload=meta
        )
        points.append(point)

    return points

def get_vector_dimension(representative_embeddings):
    """
    Get the dimension of vectors from representative embeddings.

    Parameters:
        representative_embeddings (dict): Dictionary mapping column values to embeddings

    Returns:
        int: Vector dimension
    """
    first_embedding = list(representative_embeddings.values())[0]
    return first_embedding.shape[0]
