from dataclasses import dataclass
from typing import List

from backend.vector_db.db_loader import VectorDB

@dataclass
class Doc:
    text: str
    score: float
    meta: dict

class VectorRetriever:
    def __init__(self):
        self.db = VectorDB()

    def retrieve(self, query: str, class_no: int, language: str, top_k: int = 10) -> List[Doc]:
        results = self.db.search(query, class_no=class_no, top_k=top_k, language=language)
        docs = [Doc(text=r['text'], score=r['score'], meta=r['meta']) for r in results]
        print(f"[RETRIEVAL] Found {len(docs)} chunks for query: '{query[:50]}...'")
        for i, doc in enumerate(docs[:3]):
            print(f"  Top {i+1}: score={doc.score:.3f}, text preview: {doc.text[:80]}...")
        return docs
