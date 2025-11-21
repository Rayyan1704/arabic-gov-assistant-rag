import re


def chunk_by_paragraph(text, min_chunk_size=300, max_chunk_size=800, overlap=100):
    """
    Chunk text by paragraphs with size constraints
    """
    # Split by double newline (paragraphs)
    paragraphs = text.split('\n\n')
    paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 50]
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        # If adding this paragraph keeps us under max size
        if len(current_chunk) + len(para) < max_chunk_size:
            current_chunk += "\n\n" + para if current_chunk else para
        else:
            # Save current chunk if it meets minimum
            if len(current_chunk) >= min_chunk_size:
                chunks.append(current_chunk.strip())
            
            # Start new chunk with overlap
            if overlap > 0 and current_chunk:
                # Take last 'overlap' characters from previous chunk
                overlap_text = current_chunk[-overlap:]
                current_chunk = overlap_text + "\n\n" + para
            else:
                current_chunk = para
    
    # Add final chunk
    if len(current_chunk) >= min_chunk_size:
        chunks.append(current_chunk.strip())
    
    return chunks


def chunk_document(filepath, chunk_size=512, overlap=128):
    """
    Load and chunk a single document
    IMPORTANT: Keep title/header for better retrieval
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Extract title (first line starting with #)
    lines = text.split('\n')
    title = ""
    for line in lines:
        if line.strip().startswith('#'):
            title = line.strip().replace('#', '').strip()
            break
    
    # Preprocess
    from preprocessing import normalize_arabic, clean_document
    text = clean_document(text)
    text = normalize_arabic(text)
    
    # Prepend title to text for better context
    if title:
        title_normalized = normalize_arabic(title)
        text = f"{title_normalized}\n\n{text}"
    
    # Chunk
    chunks = chunk_by_paragraph(text,
                                min_chunk_size=chunk_size-100,
                                max_chunk_size=chunk_size+100,
                                overlap=overlap)
    
    return chunks


# Test
if __name__ == "__main__":
    import glob
    files = glob.glob('../data/**/*.txt', recursive=True)
    if files:
        chunks = chunk_document(files[0])
        print(f"Created {len(chunks)} chunks")
        print(f"\nFirst chunk:\n{chunks[0][:200]}...")
