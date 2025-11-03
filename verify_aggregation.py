"""
Verify the aggregated collection and check page_content handling.

This script helps verify that aggregation worked correctly and shows
statistics about content concatenation.
"""

from qdrant_vector_aggregator.config import QDRANT_URL, QDRANT_API_KEY
from qdrant_client import QdrantClient

def main():
    print("=" * 60)
    print("Verifying Aggregated Collection")
    print("=" * 60)

    # ========================================
    # CONFIGURATION - Customize these values
    # ========================================
    collection_name = "my_documents_collection"  # Your aggregated collection name

    print(f"\n📋 Configuration:")
    print(f"  - Collection: {collection_name}")

    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=60)

    try:
        # Get collection info
        collection_info = client.get_collection(collection_name)
        print(f"\n📊 Collection: {collection_name}")
        print(f"  - Total documents: {collection_info.points_count}")

        # Get sample points
        print(f"\n📝 Sample aggregated documents:")
        points, _ = client.scroll(
            collection_name=collection_name,
            limit=3,
            with_payload=True,
            with_vectors=False
        )

        for i, point in enumerate(points, 1):
            payload = point.payload

            print(f"\n{i}. Document ID: {point.id}")
            print(f"   Payload keys: {list(payload.keys())}")

            # Check aggregation metadata
            if 'chunk_count' in payload:
                print(f"   Chunks aggregated: {payload['chunk_count']}")

            if 'has_ordered_content' in payload:
                print(f"   Has ordered content: {payload['has_ordered_content']}")

            if 'ordering_field' in payload:
                print(f"   Ordering field used: {payload['ordering_field']}")

            # Check page_content
            if 'page_content' in payload:
                content = payload['page_content']
                if content:
                    content_preview = content[:200] + "..." if len(content) > 200 else content
                    print(f"   Content length: {len(content)} characters")
                    print(f"   Content preview: {content_preview}")
                else:
                    print(f"   Content: [EMPTY - no ordering field found]")

        # Statistics
        print(f"\n📈 Content Statistics:")
        all_points, _ = client.scroll(
            collection_name=collection_name,
            limit=collection_info.points_count,
            with_payload=True,
            with_vectors=False
        )

        with_content = 0
        without_content = 0
        total_content_length = 0

        for point in all_points:
            content = point.payload.get('page_content', '')
            if content:
                with_content += 1
                total_content_length += len(content)
            else:
                without_content += 1

        print(f"  - Documents with concatenated content: {with_content}")
        print(f"  - Documents with empty content: {without_content}")
        if with_content > 0:
            avg_length = total_content_length / with_content
            print(f"  - Average content length: {avg_length:.0f} characters")

        print("\n" + "=" * 60)
        print("✅ Verification completed!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error during verification:")
        print(f"  {str(e)}")
        print(f"\n💡 Troubleshooting:")
        print(f"  1. Check that the collection exists")
        print(f"  2. Verify aggregation completed successfully")
        print(f"  3. Check your .env file has correct credentials")
        return False

    return True

if __name__ == "__main__":
    print("\n💡 Before running:")
    print("  1. Update the collection_name in this script")
    print("  2. Ensure your .env file is configured")
    print("  3. Run this after aggregation is complete\n")

    main()
