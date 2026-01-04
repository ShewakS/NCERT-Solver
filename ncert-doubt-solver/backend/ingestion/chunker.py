import re
from typing import List


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> List[str]:
    """Chunk text into chunks respecting sentence boundaries.

    Args:
        text: input text
        chunk_size: target number of characters per chunk
        overlap: number of characters to overlap
    Returns:
        List of chunk strings
    """
    # Simple accumulation by sentences
    # Split by sentence endings (.?!)
    sentences = re.split(r'(?<=[.?!])\s+', text)
    
    chunks = []
    current_chunk = []
    current_len = 0
    
    for sentence in sentences:
        s_len = len(sentence)
        if current_len + s_len > chunk_size and current_chunk:
            # Commit current chunk
            text_chunk = " ".join(current_chunk)
            chunks.append(text_chunk)
            
            # Start new with overlap logic if detailed, here simple reset with keep last if needed
            # For simplicity in this scaffold, we just start fresh or keep last sentence if crucial
            # Let's implement a rolling window style
            overlap_len = 0
            new_chunk = []
            
            # Backtrack to satisfy overlap
            for prev_s in reversed(current_chunk):
                if overlap_len + len(prev_s) < overlap:
                    new_chunk.insert(0, prev_s)
                    overlap_len += len(prev_s)
                else:
                    break
            
            current_chunk = new_chunk
            current_len = overlap_len
            
        current_chunk.append(sentence)
        current_len += s_len
        
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks
