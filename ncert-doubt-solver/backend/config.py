from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "../data"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBED_DIM = 384
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50
TOP_K = 10
VECTOR_BACKEND = "faiss"  # or 'chroma'

# Ollama Configuration
OLLAMA_API_URL = "http://localhost:11434"
OLLAMA_MODEL = "tinyllama"  # Lightweight model (1GB RAM) - fast and efficient