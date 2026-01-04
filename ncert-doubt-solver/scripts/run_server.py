"""Simple script to run FastAPI server for development"""
import uvicorn
import sys
import os

if __name__ == "__main__":
    # Add project root to path so 'backend' can be imported
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)
