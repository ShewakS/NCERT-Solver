import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from backend.ingestion.ingest_class10 import ingest_class10

if __name__ == '__main__':
    ingest_class10()
