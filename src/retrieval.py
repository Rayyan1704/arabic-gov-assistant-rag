"""Retrieval system using FAISS"""
import faiss
import numpy as np
import json
from pathlib import Path
from typing import List, Dict

class RetrieverSystem:
    """FAISS-based retrieval system with keyword boosting"""
    
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
        
        # Build keyword map for boosting
        self.keyword_map = self._build_keyword_map()
        
        print(f"✅ Index built with {self.index.ntotal} vectors")
    
    def _build_keyword_map(self):
        """Build keyword to category mapping for query boosting"""
        return {
            'حكومي': 'info',
            'hukoomi': 'info',
            'بوابة': 'info',
            'ليموزين': 'transportation',
            'limousine': 'transportation',
            'مناقصات': 'business',
            'tender': 'business',
            'كشف درجات': 'education',
            'كشف الدرجات': 'education',
            'transcript': 'education',
            'عيادة قانونية': 'justice',
            'العيادة القانونية': 'justice',
            'legal clinic': 'justice',
            'مركز قطر للمال': 'justice',
            'qfc': 'justice',
        }
    
    def _apply_keyword_boost(self, query: str, scores: np.ndarray) -> np.ndarray:
        """Boost scores based on query keywords"""
        query_lower = query.lower()
        
        for keyword, target_cat in self.keyword_map.items():
            if keyword in query_lower:
                for i, meta in enumerate(self.metadata):
                    if meta['category'] == target_cat:
                        scores[i] *= 1.5  # 50% boost
        
        return scores
    
    def search(self, query_embedding: np.ndarray, k: int = 10, query_text: str = None) -> List[Dict]:
        """
        Search for k most similar chunks
        
        Args:
            query_embedding: Query vector
            k: Number of results to return
            query_text: Original query text for keyword boosting (optional)
        
        Returns:
            List of results with scores and metadata
        """
        # Normalize query
        query_embedding = query_embedding.astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        # Get all similarities
        from sklearn.metrics.pairwise import cosine_similarity
        scores = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Apply keyword boost if query text provided
        if query_text:
            scores = self._apply_keyword_boost(query_text, scores)
        
        # Get top k
        top_indices = np.argsort(scores)[-k:][::-1]
        
        # Prepare results
        results = []
        for i, idx in enumerate(top_indices, 1):
            results.append({
                'rank': i,
                'score': float(scores[idx]),
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
