# NCERT Multilingual Doubt-Solver

This repository contains a scaffold for the NCERT Multilingual Doubt-Solver: a RAG-based system to answer students' questions using NCERT textbooks only.

## Quickstart
1. Create a Python venv and install dependencies:

   python -m venv .venv
   source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
   pip install -r backend/requirements.txt

2. Start the server for development:

   python scripts/run_server.py

3. Open `frontend/index.html` (or serve it via a static server) and test the chat.

## Next steps
- Implement FAISS/Chroma indexing and retrieval
- Integrate an LLM (OpenAI or local) for generation
- Add OCR improvements and Hindi/Urdu model support
