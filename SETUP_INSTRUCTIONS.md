# Qdrant Vector Aggregator - Setup Instructions

## Quick Setup Guide

Follow these steps to set up and use the Qdrant Vector Aggregator:

### 1. Configure Environment Variables

The library uses a `.env` file to store your Qdrant connection details.

**Option A: Edit the existing .env file**

```bash
# Open the .env file and add your Qdrant details
nano .env
```

**Option B: Copy from template**

```bash
cp .env.example .env
# Then edit .env with your details
```

### 2. Add Your Qdrant Credentials

Edit the `.env` file and add your Qdrant URL and API key:

```env
# For local Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# For Qdrant Cloud
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-api-key-here
```

### 3. Install Dependencies

```bash
# Install the package with dependencies
pip install -e . -f setup_qdrant.py

# Or install dependencies manually
pip install qdrant-client numpy scipy scikit-learn python-dotenv
```

### 4. Start Qdrant (if using local)

If you're using local Qdrant, start it with Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 5. Run the Example

Test the setup with the example script:

```bash
python example_qdrant_usage.py
```

## Usage

Once configured, you can use the library without specifying credentials:

```python
from qdrant_vector_aggregator import aggregate_embeddings

# Credentials are automatically loaded from .env
aggregate_embeddings(
    input_collection_name="my_embeddings",
    column_name="document_id",
    output_collection_name="aggregated_embeddings",
    method="average"
)
```

## Configuration Options

### Environment Variables

- `QDRANT_URL`: URL of your Qdrant server

  - Local: `http://localhost:6333`
  - Cloud: `https://your-cluster.qdrant.io`

- `QDRANT_API_KEY`: API key for Qdrant Cloud (optional for local)

  - Leave empty for local Qdrant without authentication
  - Required for Qdrant Cloud

- `DEFAULT_DISTANCE_METRIC`: Default distance metric (COSINE, EUCLIDEAN, DOT)

### Override in Code

You can still override the environment variables in your code:

```python
aggregate_embeddings(
    input_collection_name="my_embeddings",
    column_name="document_id",
    output_collection_name="aggregated_embeddings",
    method="average",
    qdrant_url="https://custom-url.qdrant.io",  # Override
    api_key="custom-api-key"  # Override
)
```

## Troubleshooting

### Connection Issues

If you get connection errors:

1. **Check Qdrant is running** (for local):

   ```bash
   docker ps | grep qdrant
   ```

2. **Verify .env file exists**:

   ```bash
   ls -la .env
   ```

3. **Check environment variables are loaded**:
   ```python
   from qdrant_vector_aggregator.config import QDRANT_URL, QDRANT_API_KEY
   print(f"URL: {QDRANT_URL}")
   print(f"API Key: {'Set' if QDRANT_API_KEY else 'Not set'}")
   ```

### Import Errors

If you get import errors:

```bash
# Make sure python-dotenv is installed
pip install python-dotenv

# Reinstall the package
pip install -e . -f setup_qdrant.py
```

## Security Notes

- **Never commit your .env file** to version control
- The `.env` file is already in `.gitignore`
- Use `.env.example` as a template for sharing
- For production, consider using environment variables or secret management services

## Next Steps

- Read the [README_QDRANT.md](README_QDRANT.md) for detailed usage examples
- Explore different aggregation methods in [example_qdrant_usage.py](example_qdrant_usage.py)
- Check the [original project](https://github.com/vinerya/faiss_vector_aggregator) for more information
