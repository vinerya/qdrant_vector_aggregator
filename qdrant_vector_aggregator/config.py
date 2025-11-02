"""
Configuration module for loading environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from the project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Qdrant configuration
QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY', None)

# Convert empty string to None for API key
if QDRANT_API_KEY == '':
    QDRANT_API_KEY = None

# Default distance metric
DEFAULT_DISTANCE_METRIC = os.getenv('DEFAULT_DISTANCE_METRIC', 'COSINE')
