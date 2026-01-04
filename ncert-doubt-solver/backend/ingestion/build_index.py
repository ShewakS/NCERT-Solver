import json
from backend.ingestion.extract_text import extract_text_from_pdf
from backend.ingestion.chunker import chunk_text
from backend.embeddings.embedder import Embedder


def build_index_for_pdf(pdf_path: str, class_no: int, output_dir: str):
    pages = extract_text_from_pdf(pdf_path)
    embedder = Embedder()
    index = []
    for p in pages:
        chunks = chunk_text(p['text'])
        for i, c in enumerate(chunks):
            emb = embedder.embed(c)
            index.append({
                'text': c,
                'meta': {'class': class_no, 'page': p['page'], 'chunk': i},
                'embedding': emb.tolist() if hasattr(emb, 'tolist') else emb,
            })
    # write out
    with open(f"{output_dir}/index.jsonl", 'w', encoding='utf-8') as f:
        for item in index:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    return len(index)
