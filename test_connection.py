"""
Test connection to Qdrant and inspect the conventions_cadre_sectorielles collection.
"""

from qdrant_vector_aggregator.config import QDRANT_URL, QDRANT_API_KEY
from qdrant_client import QdrantClient
from qdrant_client.models import Distance
import sys

def test_connection():
    """Test connection to Qdrant server."""
    print("=" * 60)
    print("Testing Qdrant Connection")
    print("=" * 60)

    # Display configuration
    print(f"\n📍 Qdrant URL: {QDRANT_URL}")
    print(f"🔑 API Key: {'Set ✓' if QDRANT_API_KEY else 'Not set ✗'}")

    try:
        # Connect to Qdrant
        print("\n🔌 Connecting to Qdrant...")
        client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        print("✓ Connection successful!")

        # List all collections
        print("\n📚 Available collections:")
        collections = client.get_collections()
        if collections.collections:
            for collection in collections.collections:
                print(f"  - {collection.name}")
        else:
            print("  No collections found")

        # Check if target collection exists
        collection_name = "conventions_cadre_sectorielles"
        print(f"\n🔍 Checking collection: {collection_name}")

        try:
            collection_info = client.get_collection(collection_name)
            print(f"✓ Collection found!")
            print(f"\n📊 Collection Details:")
            print(f"  - Name: {collection_name}")

            # Handle different vector config structures
            vectors_config = collection_info.config.params.vectors
            if isinstance(vectors_config, dict):
                # Named vectors
                vector_names = list(vectors_config.keys())
                print(f"  - Vector names: {vector_names}")
                for name, config in vectors_config.items():
                    print(f"    • {name}: size={config.size}, distance={config.distance}")
            else:
                # Single vector
                print(f"  - Vector size: {vectors_config.size}")
                print(f"  - Distance: {vectors_config.distance}")

            print(f"  - Points count: {collection_info.points_count}")
            print(f"  - Indexed vectors: {collection_info.indexed_vectors_count}")

            # Get a sample point to see the structure
            print(f"\n📝 Sample point structure:")
            points, _ = client.scroll(
                collection_name=collection_name,
                limit=1,
                with_payload=True,
                with_vectors=False
            )

            if points:
                sample_point = points[0]
                print(f"  - Point ID: {sample_point.id}")
                print(f"  - Payload keys: {list(sample_point.payload.keys())}")
                print(f"\n  Payload content:")
                for key, value in sample_point.payload.items():
                    # Truncate long values
                    value_str = str(value)
                    if len(value_str) > 100:
                        value_str = value_str[:100] + "..."
                    print(f"    • {key}: {value_str}")
            else:
                print("  No points found in collection")

            return True

        except Exception as e:
            print(f"✗ Collection not found or error accessing it")
            print(f"  Error: {str(e)}")
            return False

    except Exception as e:
        print(f"\n❌ Connection failed!")
        print(f"Error: {str(e)}")
        print("\n💡 Troubleshooting:")
        print("  1. Check your .env file has the correct QDRANT_URL")
        print("  2. Verify your QDRANT_API_KEY is correct (if using Qdrant Cloud)")
        print("  3. Make sure Qdrant is running (if using local)")
        print("     docker run -p 6333:6333 qdrant/qdrant")
        return False

def suggest_aggregation():
    """Suggest how to aggregate the collection."""
    print("\n" + "=" * 60)
    print("Suggested Aggregation Usage")
    print("=" * 60)
    print("""
To aggregate embeddings in this collection, you can use:

from qdrant_vector_aggregator import aggregate_embeddings

# Example: Aggregate by a metadata field
aggregate_embeddings(
    input_collection_name="conventions_cadre_sectorielles",
    column_name="document_id",  # Change to your grouping field
    output_collection_name="conventions_aggregated",
    method="average"  # or: pca, centroid, attentive_pooling, etc.
)

Available aggregation methods:
  • average - Simple arithmetic mean
  • weighted_average - Weighted mean (requires weights parameter)
  • pca - Principal Component Analysis
  • centroid - K-Means centroid
  • attentive_pooling - Attention-based pooling
  • max_pooling - Maximum values per dimension
  • median - Element-wise median
  • And 7 more methods!

See README_QDRANT.md for full documentation.
""")

if __name__ == "__main__":
    success = test_connection()

    if success:
        suggest_aggregation()
        print("\n✅ Connection test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Connection test failed. Please check your configuration.")
        sys.exit(1)
