"""Retrieval system using FAISS"""
import faiss
import numpy as np
import json
from pathlib import Path
from typing import List, Dict

class RetrieverSystem:
    """FAISS-based retrieval system"""
    
    def __init__(self, embeddings_path: str, chunks_path: str, metadata_path: str):
        """Initialize retriever with data"""
        # Load data
        self.embeddings = np.load(embeddings_path).astype('float32')
        
        with open(chunks_path, 'r', encoding='utf-8') as f:
            self.chunks = json.load(f)
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(self.embeddings)
        
        # Build index
        d = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(d)  # Inner product
        self.index.add(self.embeddings)
        
        print(f"✅ Index built with {self.index.ntotal} vectors")
    
    def search(self, query_embedding: np.ndarray, k: int = 10) -> List[Dict]:
        """
        Search for k most similar chunks
        
        Args:
            query_embedding: Query vector
            k: Number of results to return
        
        Returns:
            List of results with scores and metadata
        """
        # Normalize query
        query_embedding = query_embedding.astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, k)
        
        # Prepare results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            results.append({
                'rank': i + 1,
                'score': float(score),
                'chunk': self.chunks[idx],
                'metadata': self.metadata[idx]
            })
        
        return results
    
    def save_index(self, path: str):
        """Save FAISS index to disk"""
        faiss.write_index(self.index, path)
        print(f"✅ Index saved to {path}")
    
    @classmethod
    def load_index(cls, index_path: str, embeddings_path: str, 
                   chunks_path: str, metadata_path: str):
        """Load pre-built index"""
        retriever = cls(embeddings_path, chunks_path, metadata_path)
        retriever.index = faiss.read_index(index_path)
        print(f"✅ Loaded index with {retriever.index.ntotal} vectors")
        return retriever
    
    def get_stats(self) -> Dict:
        """Get retrieval system statistics"""
        from collections import Counter
        categories = Counter(m['category'] for m in self.metadata)
        
        return {
            'total_chunks': len(self.chunks),
            'total_documents': len(set(m['source_file'] for m in self.metadata)),
            'categories': dict(categories),
            'embedding_dim': self.embeddings.shape[1]
        }
