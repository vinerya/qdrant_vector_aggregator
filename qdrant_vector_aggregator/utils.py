from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import pickle
import os

def load_qdrant_collection(collection_name, qdrant_url="http://localhost:6333", api_key=None):
    """
    Load a Qdrant collection.

    Parameters:
        collection_name (str): Name of the Qdrant collection
        qdrant_url (str): URL of the Qdrant server (default: http://localhost:6333)
        api_key (str, optional): API key for Qdrant Cloud

    Returns:
        QdrantClient: Connected Qdrant client
    """
    client = QdrantClient(url=qdrant_url, api_key=api_key, timeout=120)
    return client

def save_qdrant_collection(client, collection_name, points, vector_size, distance=Distance.COSINE):
    """
    Save points to a Qdrant collection with batch upload.

    Parameters:
        client (QdrantClient): Qdrant client instance
        collection_name (str): Name of the collection to create/update
        points (list): List of PointStruct objects
        vector_size (int): Dimension of the vectors
        distance (Distance): Distance metric to use (default: COSINE)
    """
    # Recreate collection
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=distance),
    )

    # Upload points in batches to avoid timeouts
    batch_size = 100
    total_points = len(points)

    for i in range(0, total_points, batch_size):
        batch = points[i:i + batch_size]
        client.upsert(
            collection_name=collection_name,
            points=batch,
            wait=True  # Wait for each batch to complete
        )

        # Print progress
        progress = min(i + batch_size, total_points)
        print(f"  Uploaded {progress}/{total_points} points ({progress/total_points*100:.1f}%)")

def load_metadata(metadata_path):
    """Load metadata from pickle file."""
    with open(metadata_path, 'rb') as f:
        return pickle.load(f)

def save_metadata(metadata, output_path):
    """Save metadata to pickle file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        pickle.dump(metadata, f)
