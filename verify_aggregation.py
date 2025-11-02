"""
Verify the aggregated collection and check page_content handling.
"""

from qdrant_vector_aggregator.config import QDRANT_URL, QDRANT_API_KEY
from qdrant_client import QdrantClient

def main():
    print("=" * 60)
    print("Verifying Aggregated Collection")
    print("=" * 60)

    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=60)
    collection_name = "conventions_aggregated"

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

        # Check metadata
        if 'metadata' in payload and isinstance(payload['metadata'], dict):
            name = payload['metadata'].get('name', 'N/A')
            if len(name) > 70:
                name = name[:70] + "..."
            print(f"   Document name: {name}")

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

if __name__ == "__main__":
    main()
