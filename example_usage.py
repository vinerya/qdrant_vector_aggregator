"""
Example script showing how to aggregate a Qdrant collection.

This script demonstrates the basic usage of the qdrant_vector_aggregator package.
Customize the collection names and metadata field to match your data.
"""

from qdrant_vector_aggregator import aggregate_embeddings
from qdrant_vector_aggregator.config import QDRANT_URL, QDRANT_API_KEY
from qdrant_client import QdrantClient
import time

def main():
    print("=" * 60)
    print("Qdrant Vector Aggregator - Example Usage")
    print("=" * 60)

    # ========================================
    # CONFIGURATION - Customize these values
    # ========================================
    input_collection = "my_chunks_collection"      # Your input collection name
    output_collection = "my_documents_collection"  # Desired output collection name
    column_name = "metadata.document_name"         # Field to group by (e.g., document_name, doc_id, category)

    print(f"\n📋 Configuration:")
    print(f"  - Input collection: {input_collection}")
    print(f"  - Output collection: {output_collection}")
    print(f"  - Grouping by: {column_name}")
    print(f"  - Method: average (arithmetic mean)")

    # Get initial stats
    print(f"\n📊 Checking input collection...")
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    try:
        collection_info = client.get_collection(input_collection)
        initial_count = collection_info.points_count
        print(f"  - Total points: {initial_count}")

        # Start aggregation
        print(f"\n🔄 Starting aggregation...")
        print(f"  This may take a few minutes for large collections...")

        start_time = time.time()

        # Perform aggregation
        output_name, _ = aggregate_embeddings(
            input_collection_name=input_collection,
            column_name=column_name,
            output_collection_name=output_collection,
            method="average"  # Options: average, pca, attentive_pooling, etc.
        )

        elapsed_time = time.time() - start_time

        # Get final stats
        print(f"\n✅ Aggregation completed in {elapsed_time:.2f} seconds!")

        output_info = client.get_collection(output_collection)
        final_count = output_info.points_count

        print(f"\n📊 Results:")
        print(f"  - Input points: {initial_count}")
        print(f"  - Output points: {final_count}")
        print(f"  - Compression ratio: {initial_count / final_count:.2f}x")
        print(f"  - Average chunks per document: {initial_count / final_count:.1f}")

        print(f"\n💾 Output collection: {output_collection}")
        print(f"  - Ready to use for semantic search!")

        # Show sample aggregated point
        print(f"\n📝 Sample aggregated point:")
        points, _ = client.scroll(
            collection_name=output_collection,
            limit=1,
            with_payload=True,
            with_vectors=False
        )

        if points:
            sample = points[0]
            print(f"  - ID: {sample.id}")
            print(f"  - Payload keys: {list(sample.payload.keys())}")
            if 'chunk_count' in sample.payload:
                print(f"  - Chunks aggregated: {sample.payload['chunk_count']}")
            if 'has_ordered_content' in sample.payload:
                print(f"  - Content concatenated: {sample.payload['has_ordered_content']}")

        print("\n" + "=" * 60)
        print("✅ Aggregation completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error during aggregation:")
        print(f"  {str(e)}")
        print(f"\n💡 Troubleshooting:")
        print(f"  1. Check that the input collection exists")
        print(f"  2. Verify the metadata field exists in all points")
        print(f"  3. Ensure you have write permissions")
        print(f"  4. Check your .env file has correct credentials")
        return False

    return True

if __name__ == "__main__":
    print("\n💡 Before running:")
    print("  1. Update the collection names in this script")
    print("  2. Update the column_name to match your metadata field")
    print("  3. Ensure your .env file is configured\n")

    success = main()
    exit(0 if success else 1)
