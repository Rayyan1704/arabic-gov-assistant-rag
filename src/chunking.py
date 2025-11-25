"""Document chunking strategies"""
from typing import List
import re

def chunk_by_paragraph(text: str, min_chunk_size=300, max_chunk_size=800, overlap=100) -> List[str]:
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

def chunk_document(filepath: str, chunk_size=512, overlap=128) -> List[str]:
    """
    Load and chunk a single document
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Preprocess
    import re
    
    # Clean document
    text = re.sub(r'\n{3,}', '\n\n', text)
    lines = text.split('\n')
    lines = [l for l in lines if len(l.strip()) > 10]
    text = '\n'.join(lines)
    
    # Normalize Arabic
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\u0600-\u06FF\s\d\.\،\؛\؟]', '', text)
    text = text.strip()
    
    # Chunk
    chunks = chunk_by_paragraph(text,
                                min_chunk_size=chunk_size-100,
                                max_chunk_size=chunk_size+100,
                                overlap=overlap)
    
    return chunks

class DocumentChunker:
    """Handles document chunking with various strategies"""
    
    def __init__(self, chunk_size: int = 600, overlap: int = 100, min_size: int = 200):
        """
        Initialize chunker
        
        Args:
            chunk_size: Target size for each chunk in characters
            overlap: Number of characters to overlap between chunks
            min_size: Minimum chunk size to keep
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.min_size = min_size
    
    def chunk_by_paragraphs(self, text: str) -> List[str]:
        """Chunk text by paragraphs with size constraints"""
        return chunk_by_paragraph(text, self.min_size, self.chunk_size, self.overlap)
    
    def chunk_by_sentences(self, text: str) -> List[str]:
        """Chunk text by sentences (Arabic-aware)"""
        # Split by Arabic sentence endings
        sentences = re.split(r'[\.؟!]\s+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        chunks = []
        current_chunk = ""
        
        for sent in sentences:
            if len(current_chunk) + len(sent) > self.chunk_size:
                if len(current_chunk) >= self.min_size:
                    chunks.append(current_chunk.strip())
                    current_chunk = sent
                else:
                    current_chunk += " " + sent
            else:
                current_chunk += " " + sent if current_chunk else sent
        
        if len(current_chunk) >= self.min_size:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def chunk_by_sections(self, text: str) -> List[str]:
        """Chunk text by markdown sections"""
        # Split by markdown headers
        sections = re.split(r'\n##\s+', text)
        
        chunks = []
        for i, section in enumerate(sections):
            if i > 0:  # Add header back
                section = "## " + section
            
            section = section.strip()
            if len(section) >= self.min_size:
                # If section is too large, chunk it further
                if len(section) > self.chunk_size * 1.5:
                    sub_chunks = self.chunk_by_paragraphs(section)
                    chunks.extend(sub_chunks)
                else:
                    chunks.append(section)
        
        return chunks
    
    def chunk_document(self, text: str, strategy: str = 'paragraphs') -> List[str]:
        """
        Chunk document using specified strategy
        
        Args:
            text: Document text
            strategy: 'paragraphs', 'sentences', or 'sections'
        
        Returns:
            List of text chunks
        """
        if strategy == 'paragraphs':
            return self.chunk_by_paragraphs(text)
        elif strategy == 'sentences':
            return self.chunk_by_sentences(text)
        elif strategy == 'sections':
            return self.chunk_by_sections(text)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

# Test
if __name__ == "__main__":
    import glob
    files = glob.glob('data/health/*.txt')
    if files:
        chunks = chunk_document(files[0])
        print(f"Created {len(chunks)} chunks")
        print(f"\nFirst chunk:\n{chunks[0][:200]}...")
