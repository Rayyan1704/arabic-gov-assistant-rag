"""
Category-specific retrieval with per-category FAISS indexes
"""
import faiss
import numpy as np
import json
from sentence_transformers import CrossEncoder


class CategoryRetriever:
    def __init__(self, embeddings_path, chunks_path, metadata_path):
        """Initialize category-specific retrieval system"""
        # Load data
        self.embeddings = np.load(embeddings_path).astype('float32')
        
        with open(chunks_path, 'r', encoding='utf-8') as f:
            self.chunks = json.load(f)
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
        
        # Normalize
        faiss.normalize_L2(self.embeddings)
        
        # Get unique categories
        self.categories = list(set(m['category'] for m in self.metadata))
        
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
            
            print(f"✅ Built index for {cat}: {len(cat_indices)} chunks")
        
        # Build global index too
        d = self.embeddings.shape[1]
        self.global_index = faiss.IndexFlatIP(d)
        self.global_index.add(self.embeddings)
        print(f"✅ Built global index: {len(self.chunks)} chunks")
    
    def detect_category(self, query):
        """
        Simple keyword-based category detection
        """
        query = query.lower()
        
        # Define keywords per category
        category_keywords = {
            'health': ['صحة', 'طبيب', 'مستشفى', 'علاج', 'دواء', 'طبي', 'حمد', 'استشارة', 'تقرير'],
            'education': ['مدرسة', 'تعليم', 'جامعة', 'طالب', 'دراسة', 'تسجيل', 'مقررات', 'قبول', 'كشف'],
            'business': ['شركة', 'تجاري', 'سجل', 'رخصة', 'استثمار', 'تمويل', 'مناقصات', 'ضرائب'],
            'transportation': ['سيارة', 'قيادة', 'مرور', 'نقل', 'ليموزين', 'شحن', 'مركبة', 'تأجير'],
            'justice': ['محكمة', 'قضاء', 'دعوى', 'مرافعة', 'قانون', 'عدل'],
            'housing': ['سكن', 'منزل', 'ملكية', 'سند', 'إسكان'],
            'culture': ['ثقافة', 'فن', 'تصوير', 'أفلام', 'إعلام'],
            'info': ['معلومات', 'حكومي', 'استبيان', 'شارك', 'حكوي']
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
        Search in specific category or globally
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


class RerankedRetriever(CategoryRetriever):
    """Retriever with cross-encoder reranking"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Load cross-encoder model
        print("Loading cross-encoder for reranking...")
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        print("✅ Reranker loaded")
    
    def search_with_rerank(self, query, query_embedding, category=None,
                          initial_k=20, final_k=5):
        """
        Two-stage retrieval: fast search + reranking
        
        Stage 1: Get initial candidates with embeddings (fast)
        Stage 2: Rerank with cross-encoder (accurate)
        """
        # Stage 1: Get initial candidates
        candidates = self.search(query_embedding, category=category, k=initial_k)
        
        # Stage 2: Rerank with cross-encoder
        pairs = [[query, c['chunk']] for c in candidates]
        rerank_scores = self.reranker.predict(pairs)
        
        # Add rerank scores
        for i, candidate in enumerate(candidates):
            candidate['rerank_score'] = float(rerank_scores[i])
            candidate['original_score'] = candidate['score']
        
        # Sort by rerank scores
        candidates.sort(key=lambda x: x['rerank_score'], reverse=True)
        
        # Update ranks
        for i, c in enumerate(candidates[:final_k], 1):
            c['rank'] = i
        
        return candidates[:final_k]
