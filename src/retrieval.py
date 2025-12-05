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
        
        # Extract titles for title matching
        self.titles = self._extract_titles()
        
        print(f"✅ Index built with {self.index.ntotal} vectors")
    
    def _extract_titles(self):
        """Extract service titles from chunks"""
        titles = []
        for chunk in self.chunks:
            lines = chunk.split('\n')
            title = lines[0] if lines else ""
            titles.append(title.strip())
        return titles
    
    def _title_similarity(self, query: str, title: str) -> float:
        """Calculate title similarity score"""
        query_lower = query.lower()
        title_lower = title.lower()
        
        # Exact substring match
        if query_lower in title_lower or title_lower in query_lower:
            return 1.0
        
        # Word overlap
        query_words = set(query_lower.split())
        title_words = set(title_lower.split())
        
        if not query_words or not title_words:
            return 0.0
        
        overlap = len(query_words & title_words)
        return overlap / max(len(query_words), len(title_words))
    
    def _build_keyword_map(self):
        """Build keyword to category mapping for query boosting"""
        return {
            # Education - TRANSCRIPT SPECIFIC (HIGHEST PRIORITY)
            'transcript request': 'education',
            'transcript': 'education',
            'طلب نسخة': 'education',  # Translation of "transcript request"
            'كشف درجات': 'education',
            'كشف الدرجات': 'education',
            'نسخة درجات': 'education',
            'طلب كشف': 'education',
            'grades transcript': 'education',
            'academic transcript': 'education',
            'university transcript': 'education',
            'نسخة الجامعة': 'education',  # Translation of "university transcript"
            'كيفية طلب نسخة': 'education',  # Translation of "how to request transcript"
            'جامعة قطر': 'education',
            'qatar university': 'education',
            'جامعة': 'education',
            'university': 'education',
            'مدرسة': 'education',
            'school': 'education',
            'تسجيل': 'education',
            'admission': 'education',
            'طلاب': 'education',
            'student': 'education',
            'grades': 'education',
            'درجات': 'education',
            
            # Info
            'حكومي': 'info',
            'hukoomi': 'info',
            'بوابة': 'info',
            'portal': 'info',
            'about': 'info',
            'خدمات': 'info',
            
            # Transportation
            'ليموزين': 'transportation',
            'limousine': 'transportation',
            'قيادة': 'transportation',
            'سواقة': 'transportation',
            'driving': 'transportation',
            'رخصة قيادة': 'transportation',
            'نقل': 'transportation',
            'transport': 'transportation',
            'license': 'transportation',
            
            # Business
            'مناقصات': 'business',
            'tender': 'business',
            'تجارية': 'business',
            'business': 'business',
            'رخصة تجارية': 'business',
            'patent': 'business',
            'براءة': 'business',
            
            # Justice
            'بوابة المحامين': 'justice',
            'lawyers portal': 'justice',
            'محامي': 'justice',
            'lawyer': 'justice',
            'قضية': 'justice',
            'case': 'justice',
            'محكمة': 'justice',
            'court': 'justice',
            'نيابة': 'justice',
            'attorney': 'justice',
            'قانوني': 'justice',
            'legal': 'justice',
            
            # Health
            'دكتور': 'health',
            'doctor': 'health',
            'ممرض': 'health',
            'nurse': 'health',
            'طبيب': 'health',
            'صحة': 'health',
            'health': 'health',
            
            # Housing
            'بدل ايجار': 'housing',
            'rent allowance': 'housing',
            'ايجار': 'housing',
            'rent': 'housing',
            'سكن': 'housing',
            'housing': 'housing',
            
            # Culture
            'ثقافة': 'culture',
            'culture': 'culture',
            'متحف': 'culture',
            'museum': 'culture',
        }
    
    def _direct_filename_match(self, query: str):
        """Check for direct filename pattern matches
        
        Returns:
            int: Index of matching document, or None if no match
        """
        query_lower = query.lower()
        
        # Direct mappings for specific queries
        direct_patterns = {
            'legal clinic': 'legal_clinic',
            'qfc': 'legal_clinic',
            'العيادة القانونية': 'legal_clinic',
            'مركز قطر للمال': 'legal_clinic',
            'transcript': 'transcript',
            'كشف درجات': 'transcript',
            'كشف الدرجات': 'transcript',
        }
        
        for pattern, filename_part in direct_patterns.items():
            if pattern in query_lower:
                for i, meta in enumerate(self.metadata):
                    if filename_part in meta['source_file'].lower():
                        return i
        
        return None
    
    def search(self, query_embedding: np.ndarray, k: int = 10, query_text: str = None) -> List[Dict]:
        """
        Search for k most similar chunks with title matching
        
        Args:
            query_embedding: Query vector
            k: Number of results to return
            query_text: Original query text for keyword boosting and title matching (optional)
        
        Returns:
            List of results with scores and metadata
        """
        # Normalize query
        query_embedding = query_embedding.astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        # Get all similarities
        from sklearn.metrics.pairwise import cosine_similarity
        semantic_scores = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # If query text provided, enhance with title matching
        if query_text:
            # Check for direct filename match first
            direct_match_idx = self._direct_filename_match(query_text)
            
            # Title matching scores
            title_scores = np.array([
                self._title_similarity(query_text, title) 
                for title in self.titles
            ])
            
            # Keyword boosting
            keyword_boost = np.ones(len(self.chunks))
            query_lower = query_text.lower()
            
            # Check for multi-word phrases first (more specific)
            for keyword, target_cat in sorted(self.keyword_map.items(), key=lambda x: -len(x[0])):
                if keyword.lower() in query_lower:
                    for i, meta in enumerate(self.metadata):
                        if meta['category'] == target_cat:
                            # Apply boost
                            keyword_boost[i] = max(keyword_boost[i], 2.0)
            
            # If direct match found, boost it heavily
            if direct_match_idx is not None:
                keyword_boost[direct_match_idx] = 10.0  # Very strong boost
            
            # Combined scoring with additive keyword boost
            # - Semantic similarity (50%)
            # - Title match (20%)
            # - Keyword boost (30% - additive, not multiplicative)
            keyword_bonus = (keyword_boost - 1.0) * 0.3  # Convert boost to bonus
            final_scores = (
                0.50 * semantic_scores +
                0.20 * title_scores +
                keyword_bonus
            )
        else:
            # No query text, use semantic only
            final_scores = semantic_scores
        
        # Get top k
        top_indices = np.argsort(final_scores)[-k:][::-1]
        
        # Prepare results
        results = []
        for i, idx in enumerate(top_indices, 1):
            results.append({
                'rank': i,
                'score': float(final_scores[idx]),
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
