import os
import json
from pathlib import Path
import numpy as np
import faiss

from backend.embeddings.embedder import Embedder

class VectorDB:
    def __init__(self, base_dir: str | None = None):
        # base_dir should point to repository data folder
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path(__file__).resolve().parents[2] / 'data'
        self.indexes = {}
        self.metadatas = {}
        self.embedder = Embedder()

    def load_index(self, class_no: int):
        if class_no in self.indexes:
            return self.indexes[class_no]
        idx_dir = self.base_dir / f'class_{class_no}' / 'vector_db'
        index_path = idx_dir / 'index.faiss'
        meta_path = idx_dir / 'metadata.jsonl'
        if not index_path.exists() or not meta_path.exists():
            raise FileNotFoundError(f"Index or metadata not found for class {class_no} in {idx_dir}")
        index = faiss.read_index(str(index_path))
        metas = []
        with open(meta_path, 'r', encoding='utf-8') as f:
            for line in f:
                metas.append(json.loads(line))
        self.indexes[class_no] = index
        self.metadatas[class_no] = metas
        return index

    def search(self, query: str, class_no: int, top_k: int = 5, language: str = 'en'):
        index = self.load_index(class_no)
        metas = self.metadatas[class_no]
        emb = self.embedder.embed(query)
        x = np.array([emb], dtype='float32')
        faiss.normalize_L2(x)
        D, I = index.search(x, top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(metas):
                continue
            m = metas[idx]
            results.append({'text': m.get('text'), 'score': float(score), 'meta': m.get('meta')})
        return results
