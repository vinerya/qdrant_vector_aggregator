"""
Debug script to check aggregation process step by step.

This script helps troubleshoot aggregation issues by showing detailed
information about the collection and aggregation process.
"""

from qdrant_vector_aggregator.config import QDRANT_URL, QDRANT_API_KEY
from qdrant_client import QdrantClient
import numpy as np

def main():
    print("=" * 60)
    print("Debug Aggregation Process")
    print("=" * 60)

    # ========================================
    # CONFIGURATION - Customize these values
    # ========================================
    collection_name = "my_chunks_collection"  # Your collection name
    column_name = "metadata.document_name"    # Field to group by

    print(f"\n📋 Configuration:")
    print(f"  - Collection: {collection_name}")
    print(f"  - Grouping by: {column_name}")

    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=60)

    print(f"\n1️⃣ Collecting embeddings by '{column_name}'...")

    embeddings_by_column = {}
    metadata_by_column = {}

    offset = None
    limit = 100
    total_processed = 0

    try:
        while True:
            points, next_offset = client.scroll(
                collection_name=collection_name,
                limit=limit,
                offset=offset,
                with_payload=True,
                with_vectors=True
            )

            if not points:
                break

            for point in points:
                payload = point.payload
                vector = point.vector

                # Extract column value (handles nested fields)
                column_value = None
                if '.' in column_name:
                    # Handle nested fields like "metadata.document_name"
                    parts = column_name.split('.')
                    value = payload
                    for part in parts:
                        if isinstance(value, dict) and part in value:
                            value = value[part]
                        else:
                            value = None
                            break
                    column_value = value
                else:
                    # Handle top-level fields
                    column_value = payload.get(column_name)

                if column_value is not None:
                    if column_value not in embeddings_by_column:
                        embeddings_by_column[column_value] = []
                        metadata_by_column[column_value] = payload

                    embeddings_by_column[column_value].append(vector)

            total_processed += len(points)
            print(f"  Processed {total_processed} points...")

            if next_offset is None:
                break
            offset = next_offset

        print(f"\n2️⃣ Aggregation Summary:")
        print(f"  - Total points processed: {total_processed}")
        print(f"  - Unique groups found: {len(embeddings_by_column)}")
        if len(embeddings_by_column) > 0:
            print(f"  - Compression ratio: {total_processed / len(embeddings_by_column):.2f}x")

        print(f"\n3️⃣ Sample groups:")
        for i, (group_name, vectors) in enumerate(list(embeddings_by_column.items())[:5]):
            group_name_short = str(group_name)[:60] + "..." if len(str(group_name)) > 60 else str(group_name)
            print(f"  {i+1}. {group_name_short}")
            print(f"     Chunks: {len(vectors)}")

        if len(embeddings_by_column) > 0:
            print(f"\n4️⃣ Computing average embeddings...")
            representative_embeddings = {}
            for column_value, vectors in embeddings_by_column.items():
                vectors_array = np.array(vectors)
                representative_embeddings[column_value] = np.mean(vectors_array, axis=0)

            print(f"  ✓ Computed {len(representative_embeddings)} representative embeddings")
            print(f"  Vector dimension: {len(next(iter(representative_embeddings.values())))}")

        print("\n" + "=" * 60)
        print("✅ Debug completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error during debug:")
        print(f"  {str(e)}")
        print(f"\n💡 Troubleshooting:")
        print(f"  1. Check that the collection exists")
        print(f"  2. Verify the column_name field exists in your data")
        print(f"  3. Check your .env file has correct credentials")
        return False

    return True

if __name__ == "__main__":
    print("\n💡 Before running:")
    print("  1. Update the collection_name in this script")
    print("  2. Update the column_name to match your metadata field")
    print("  3. Ensure your .env file is configured\n")

    main()
