import json
from pathlib import Path
from tqdm import tqdm
import numpy as np
import faiss
import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.ingestion.extract_text import extract_text_from_pdf
from backend.ingestion.chunker import chunk_text
from backend.embeddings.embedder import Embedder
from backend.config import CHUNK_SIZE, CHUNK_OVERLAP

DATA_ROOT = Path(__file__).resolve().parents[2] / 'data' / 'class_10'


def ingest_class10(pdfs_root: Path = None):
    pdfs_root = pdfs_root or DATA_ROOT
    extracted_root = pdfs_root / 'extracted_text'
    chunks_root = pdfs_root / 'chunks'
    vector_root = pdfs_root / 'vector_db'

    extracted_root.mkdir(parents=True, exist_ok=True)
    chunks_root.mkdir(parents=True, exist_ok=True)
    vector_root.mkdir(parents=True, exist_ok=True)

    embedder = Embedder()

    all_chunks = []

    # iterate subject folders
    for subject_dir in sorted(pdfs_root.iterdir()):
        if not subject_dir.is_dir():
            continue
        if subject_dir.name in ['vector_db', 'extracted_text', 'chunks'] or subject_dir.name.startswith('.'):
            continue
        subject = subject_dir.name
        out_subject_dir = extracted_root / subject
        out_subject_dir.mkdir(parents=True, exist_ok=True)

        pdfs = list(subject_dir.glob('*.pdf'))
        for pdf in pdfs:
            print(f"Processing {subject}/{pdf.name}")
            pages = extract_text_from_pdf(str(pdf))
            # save raw extracted pages
            out_file = out_subject_dir / (pdf.stem + '.json')
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(pages, f, ensure_ascii=False, indent=2)

            for p in pages:
                text = (p.get('text') or '').strip()
                if not text:
                    continue
                chunks = chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
                for i, c in enumerate(chunks):
                    meta = {
                        'class': 10,
                        'subject': subject,
                        'source_pdf': pdf.name,
                        'page': p.get('page'),
                        'chunk_id': i,
                    }
                    all_chunks.append({'text': c, 'meta': meta})

    if not all_chunks:
        print("No chunks found for Class 10. Check if PDFs exist in subject folders.")
        return

    # save chunks file
    chunks_file = chunks_root / 'chunks.jsonl'
    print(f"Writing {len(all_chunks)} chunks to {chunks_file}")
    with open(chunks_file, 'w', encoding='utf-8') as f:
        for item in all_chunks:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    # create embeddings in batches
    texts = [c['text'] for c in all_chunks]
    batch_size = 128
    embeddings = []
    for i in tqdm(range(0, len(texts), batch_size), desc='Embedding'):
        batch = texts[i:i+batch_size]
        emb = embedder.embed_batch(batch)
        embeddings.append(emb)
    
    if embeddings:
        embeddings = np.vstack(embeddings).astype('float32')
    else:
        embeddings = np.zeros((0, 0), dtype='float32')

    if embeddings.size == 0:
        print('No embeddings created, aborting index build.')
        return

    # normalize for cosine similarity with inner product
    faiss.normalize_L2(embeddings)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    index_path = vector_root / 'index.faiss'
    faiss.write_index(index, str(index_path))
    print(f'FAISS index saved to {index_path}')

    # save metadata (including chunk text)
    meta_path = vector_root / 'metadata.jsonl'
    with open(meta_path, 'w', encoding='utf-8') as f:
        for item in all_chunks:
            entry = {'text': item['text'], 'meta': item['meta']}
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    info = {'n_chunks': len(all_chunks), 'dim': dim}
    with open(vector_root / 'index_info.json', 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    print('Ingestion for Class 10 complete.')


if __name__ == '__main__':
    ingest_class10()
