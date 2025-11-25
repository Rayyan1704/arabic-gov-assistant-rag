"""
Category-specific retrieval with per-category FAISS indexes.
Allows searching within specific document categories for better precision.
"""

import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer


class CategoryRetriever:
    def __init__(self, embeddings_path, chunks_path, metadata_path):
        """
        Initialize retriever with per-category FAISS indexes.
        
        Args:
            embeddings_path: Path to embeddings.npy
            chunks_path: Path to corpus_chunks.json
            metadata_path: Path to corpus_meta.json
        """
        print("Loading data...")
        # Load data
        self.embeddings = np.load(embeddings_path).astype('float32')
        
        with open(chunks_path, 'r', encoding='utf-8') as f:
            self.chunks = json.load(f)
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
        
        print(f"✅ Loaded {len(self.chunks)} chunks")
        
        # Normalize embeddings
        faiss.normalize_L2(self.embeddings)
        
        # Get unique categories
        self.categories = list(set(m['category'] for m in self.metadata))
        print(f"✅ Found {len(self.categories)} categories: {self.categories}")
        
        # Build per-category indexes
        self.category_indexes = {}
        self.category_mappings = {}  # Maps local idx -> global idx
        
        for cat in self.categories:
            # Get indices for this category
            cat_indices = [i for i, m in enumerate(self.metadata) if m['category'] == cat]
            
            # Get embeddings for this category
            cat_embeddings = self.embeddings[cat_indices]
            
            # Build index
            d = cat_embeddings.shape[1]
            index = faiss.IndexFlatIP(d)
            index.add(cat_embeddings)
            
            self.category_indexes[cat] = index
            self.category_mappings[cat] = cat_indices
            
            print(f"✅ Built index for '{cat}': {len(cat_indices)} chunks")
        
        # Build global index too
        d = self.embeddings.shape[1]
        self.global_index = faiss.IndexFlatIP(d)
        self.global_index.add(self.embeddings)
        print(f"✅ Built global index: {len(self.chunks)} chunks")
    
    def detect_category(self, query):
        """
        Simple keyword-based category detection.
        
        Args:
            query: Query string
            
        Returns:
            Detected category name or None
        """
        query = query.lower()
        
        # Define keywords per category (Arabic)
        category_keywords = {
            'health': ['صحة', 'طبيب', 'مستشفى', 'علاج', 'دواء', 'بطاقة صحية', 'مريض', 'عيادة'],
            'education': ['مدرسة', 'تعليم', 'جامعة', 'طالب', 'دراسة', 'تسجيل', 'معهد', 'تعليمي'],
            'business': ['شركة', 'تجاري', 'سجل', 'رخصة عمل', 'استثمار', 'تجارة', 'أعمال'],
            'transportation': ['سيارة', 'قيادة', 'رخصة', 'مرور', 'نقل', 'مركبة', 'طريق'],
            'housing': ['سكن', 'منزل', 'عقار', 'إيجار', 'شقة', 'بناء'],
            'justice': ['قانون', 'محكمة', 'عدل', 'قضاء', 'حق', 'دعوى'],
            'culture': ['ثقافة', 'فن', 'تراث', 'متحف', 'معرض'],
            'info': ['معلومات', 'خدمة', 'إجراء', 'وثيقة']
        }
        
        scores = {}
        for cat, keywords in category_keywords.items():
            if cat in self.categories:
                score = sum(1 for kw in keywords if kw in query)
                scores[cat] = score
        
        # Return category with highest score, or None
        if scores and max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return None
    
    def search(self, query_embedding, category=None, k=10):
        """
        Search in specific category or globally.
        
        Args:
            query_embedding: Query embedding vector
            category: Category to search in (None for global search)
            k: Number of results to return
            
        Returns:
            List of result dictionaries
        """
        query_embedding = query_embedding.astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        if category and category in self.category_indexes:
            # Search in category-specific index
            index = self.category_indexes[category]
            mapping = self.category_mappings[category]
            
            scores, local_indices = index.search(query_embedding, min(k, len(mapping)))
            
            # Convert local indices to global
            global_indices = [mapping[i] for i in local_indices[0]]
            
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], global_indices)):
                results.append({
                    'rank': i + 1,
                    'score': float(score),
                    'chunk': self.chunks[idx],
                    'metadata': self.metadata[idx],
                    'search_type': f'category:{category}'
                })
        else:
            # Search globally
            scores, indices = self.global_index.search(query_embedding, k)
            
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                results.append({
                    'rank': i + 1,
                    'score': float(score),
                    'chunk': self.chunks[idx],
                    'metadata': self.metadata[idx],
                    'search_type': 'global'
                })
        
        return results



from sentence_transformers import CrossEncoder


class RerankedRetriever(CategoryRetriever):
    """
    Enhanced retriever with cross-encoder reranking.
    Two-stage retrieval: fast embedding search + accurate cross-encoder reranking.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Load cross-encoder model
        print("\nLoading cross-encoder for reranking...")
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        print("✅ Reranker loaded")
    
    def search_with_rerank(self, query, query_embedding, category=None,
                          initial_k=20, final_k=5):
        """
        Two-stage retrieval: fast search + reranking.
        
        Args:
            query: Query text (needed for cross-encoder)
            query_embedding: Query embedding vector
            category: Category to search in (None for global)
            initial_k: Number of candidates to retrieve initially
            final_k: Number of results to return after reranking
            
        Returns:
            List of reranked result dictionaries
        """
        # Stage 1: Get initial candidates with fast embedding search
        candidates = self.search(query_embedding, category=category, k=initial_k)
        
        if not candidates:
            return []
        
        # Stage 2: Rerank with cross-encoder
        pairs = [[query, c['chunk']] for c in candidates]
        rerank_scores = self.reranker.predict(pairs)
        
        # Add rerank scores to candidates
        for i, candidate in enumerate(candidates):
            candidate['rerank_score'] = float(rerank_scores[i])
            candidate['original_score'] = candidate['score']
        
        # Sort by rerank scores
        candidates.sort(key=lambda x: x['rerank_score'], reverse=True)
        
        # Update ranks
        for i, c in enumerate(candidates[:final_k], 1):
            c['rank'] = i
        
        return candidates[:final_k]
