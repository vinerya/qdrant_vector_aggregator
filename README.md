# Qdrant Vector Aggregator

A Python library for aggregating embeddings in Qdrant collections with **smart content concatenation**. Reduce your vector database size while maintaining semantic search quality and preserving complete document content.

## 🌟 Key Features

- **14 Aggregation Methods**: Average, PCA, attention-based pooling, and more
- **Smart Content Concatenation**: Automatically detects chunk ordering and concatenates text in proper sequence
- **Qdrant Cloud & Local Support**: Works with both cloud and self-hosted instances
- **Batch Processing**: Efficient handling of large collections with progress tracking
- **Flexible Grouping**: Aggregate by any metadata field (document name, ID, category, etc.)
- **Production Ready**: Includes error handling, logging, and verification tools

## 📊 What It Does

Transform chunked embeddings into document-level embeddings:

```
Input Collection (many chunks)
├── Document A - Chunk 1 (embedding + text)
├── Document A - Chunk 2 (embedding + text)
├── Document A - Chunk 3 (embedding + text)
├── Document B - Chunk 1 (embedding + text)
└── ...

                    ↓ Aggregate

Output Collection (fewer documents)
├── Document A (averaged embedding + concatenated text)
├── Document B (averaged embedding + concatenated text)
└── ...
```

**Result**: Significant compression with preserved semantic meaning and complete document text!

## 🚀 Quick Start

### Installation

```bash
# Clone or download this repository
cd qdrant_vector_aggregator

# Install dependencies
pip install qdrant-client numpy scikit-learn python-dotenv
```

### Configuration

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` with your Qdrant credentials:

```bash
QDRANT_URL=https://your-cluster.cloud.qdrant.io
QDRANT_API_KEY=your-api-key-here
```

### Basic Usage

```python
from qdrant_vector_aggregator import aggregate_embeddings

# Aggregate embeddings by document name
aggregate_embeddings(
    input_collection_name="my_chunks_collection",
    column_name="metadata.document_name",  # Field to group by
    output_collection_name="my_documents_collection",
    method="average"  # Aggregation method
)
```

## 🎯 Smart Content Concatenation

The aggregator automatically handles `page_content` concatenation:

### How It Works

1. **Detects Ordering Fields**: Checks for common ordering fields:

   - `chunk_index`, `chunk_number`, `chunk_id`
   - `page`, `page_number`, `page_num`
   - `sequence`, `order`, `index`, `position`
   - `id` (if sequential)

2. **Sorts & Concatenates**: If ordering found, sorts chunks and concatenates text in proper order

3. **Adds Metadata**: Includes aggregation statistics:
   - `chunk_count`: Number of chunks aggregated
   - `has_ordered_content`: Whether content was concatenated
   - `ordering_field`: Which field was used for ordering

### Example Result

```python
{
    "page_content": "Chapter 1...\n\nChapter 2...\n\nChapter 3...",  # Concatenated in order
    "metadata": {
        "name": "Document Title",
        "id": 12345
    },
    "chunk_count": 34,
    "has_ordered_content": True,
    "ordering_field": "metadata.id"
}
```

If no ordering field is found, `page_content` is set to empty string.

## 📚 Available Aggregation Methods

| Method              | Description                  | Best For                              |
| ------------------- | ---------------------------- | ------------------------------------- |
| `average`           | Arithmetic mean (default)    | General purpose, balanced             |
| `weighted_average`  | Weighted mean                | When chunks have different importance |
| `pca`               | Principal Component Analysis | Dimensionality reduction              |
| `centroid`          | K-Means centroid             | Cluster-based aggregation             |
| `attentive_pooling` | Attention-based pooling      | Context-aware aggregation             |
| `max_pooling`       | Maximum values per dimension | Highlighting key features             |
| `min_pooling`       | Minimum values per dimension | Conservative aggregation              |
| `median`            | Element-wise median          | Robust to outliers                    |
| `trimmed_mean`      | Mean after trimming extremes | Outlier-resistant                     |
| `geometric_mean`    | Geometric mean               | Multiplicative relationships          |
| `harmonic_mean`     | Harmonic mean                | Rate-based data                       |
| `power_mean`        | Generalized mean             | Flexible aggregation                  |
| `soft_dtw`          | Soft Dynamic Time Warping    | Sequence alignment                    |
| `procrustes`        | Procrustes analysis          | Shape-based alignment                 |

## 🛠️ Included Tools

### 1. Test Connection

```bash
python3 test_connection.py
```

Verifies Qdrant connection and displays available collections.

### 2. Example Usage

```bash
python3 example_usage.py
```

Example script showing how to aggregate a collection.

### 3. Verify Aggregation

```bash
python3 verify_aggregation.py
```

Checks aggregation results and content concatenation statistics.

### 4. Debug Aggregation

```bash
python3 debug_aggregation.py
```

Detailed debugging information for troubleshooting.

## 📖 Advanced Usage

### Custom Aggregation

```python
from qdrant_vector_aggregator import aggregate_embeddings
from qdrant_client.models import Distance

# PCA-based aggregation with custom settings
aggregate_embeddings(
    input_collection_name="source_collection",
    column_name="metadata.category",
    output_collection_name="aggregated_collection",
    method="pca",
    distance_metric=Distance.COSINE,
    qdrant_url="https://your-cluster.cloud.qdrant.io",
    api_key="your-api-key"
)
```

### Weighted Average

```python
# Aggregate with custom weights (e.g., by chunk importance)
aggregate_embeddings(
    input_collection_name="source_collection",
    column_name="metadata.document_id",
    output_collection_name="weighted_collection",
    method="weighted_average",
    weights=[0.5, 0.3, 0.2]  # Weights for first 3 chunks
)
```

### Attention-Based Pooling

```python
# Context-aware aggregation
aggregate_embeddings(
    input_collection_name="source_collection",
    column_name="metadata.document_id",
    output_collection_name="attention_collection",
    method="attentive_pooling"
)
```

## 🔍 Searching Aggregated Collections

```python
from qdrant_client import QdrantClient

client = QdrantClient(url="your-url", api_key="your-key")

# Search the aggregated collection
results = client.search(
    collection_name="aggregated_collection",
    query_vector=your_query_embedding,  # 1536-dim vector
    limit=5
)

# Each result now represents a complete document
for result in results:
    print(f"Document: {result.payload['metadata']['name']}")
    print(f"Score: {result.score}")
    print(f"Chunks: {result.payload['chunk_count']}")
    print(f"Content: {result.payload['page_content'][:200]}...")
```

## 📁 Project Structure

```
qdrant_vector_aggregator/
├── .env                          # Your credentials (not in git)
├── .env.example                  # Template
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
├── SETUP_INSTRUCTIONS.md         # Detailed setup guide
├── LICENSE                       # MIT License
├── setup.py                      # Installation script
│
├── qdrant_vector_aggregator/     # Main package
│   ├── __init__.py              # Package initialization
│   ├── aggregator.py            # Core aggregation logic
│   ├── config.py                # Configuration management
│   ├── embedding_methods.py     # All 14 aggregation methods
│   ├── qdrant_collection_helpers.py  # Qdrant utilities
│   └── utils.py                 # Helper functions
│
├── test_connection.py           # Connection testing
├── example_usage.py             # Usage examples
├── debug_aggregation.py         # Debugging tool
└── verify_aggregation.py        # Verification tool
```

## 🎓 Real-World Example

```python
from qdrant_vector_aggregator import aggregate_embeddings

# Aggregate document chunks into complete documents
result = aggregate_embeddings(
    input_collection_name="my_document_chunks",
    column_name="metadata.document_name",  # Group by document name
    output_collection_name="my_complete_documents",
    method="average"
)

# Example results:
# ✅ Significant compression ratio
# ✅ Content automatically concatenated in proper order
# ✅ Semantic meaning preserved
# ✅ Ready for document-level semantic search
```

## 🔧 Troubleshooting

### Connection Issues

```bash
# Test your connection
python3 test_connection.py
```

### Timeout Errors

The aggregator uses batch processing (100 points per batch) to prevent timeouts. For very large collections, you can adjust the batch size in `utils.py`.

### Content Not Concatenating

Run the verification tool to check:

```bash
python3 verify_aggregation.py
```

This will show:

- Which ordering field was detected (if any)
- How many documents have concatenated content
- Average content length

## 📝 Requirements

- Python 3.7+
- qdrant-client
- numpy
- scikit-learn
- python-dotenv

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Add new aggregation methods
- Improve content concatenation logic
- Add more examples
- Report issues

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

Based on the original [faiss_vector_aggregator](https://github.com/vinerya/faiss_vector_aggregator) project, adapted for Qdrant with enhanced features including smart content concatenation.

## 🔗 Repository

GitHub: [qdrant_vector_aggregator](https://github.com/vinerya/qdrant_vector_aggregator)

## 📞 Support

For issues or questions:

1. Check `SETUP_INSTRUCTIONS.md` for detailed setup help
2. Run `debug_aggregation.py` for troubleshooting
3. Review the example scripts for usage patterns

---

**Made with ❤️ for the Qdrant community**
