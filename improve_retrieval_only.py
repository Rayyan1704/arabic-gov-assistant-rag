"""
Improve retrieval without changing chunks
Focus on query-side improvements
"""

import sys
import os
sys.path.insert(0, 'src')

import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from sklearn.metrics.pairwise import cosine_similarity
import re


class SmartQueryProcessor:
    """Improved query processing"""
    
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    def normalize_query(self, query: str) -> str:
        """Light normalization"""
        query = re.sub(r'[\u064B-\u065F\u0670]', '', query)
        query = re.sub(r'[إأآ]', 'ا', query)
        query = re.sub(r'\s+', ' ', query)
        return query.strip()
    
    def expand_with_synonyms(self, query: str) -> list:
        """Expand with Arabic synonyms"""
        variations = [query]
        
        # More comprehensive synonyms
        replacements = [
            ('رخصة', 'ترخيص'),
            ('ترخيص', 'رخصة'),
            ('تصريح', 'رخصة'),
            ('طلب', 'تقديم'),
            ('كيف أحصل', 'كيف احصل'),
            ('كيف أحصل', 'طريقة الحصول'),
            ('ما هي', 'ماهي'),
        ]
        
        for old, new in replacements:
            if old in query:
                variations.append(query.replace(old, new))
        
        return list(set(variations))[:3]
    
    def extract_keywords(self, query: str) -> list:
        """Extract key terms"""
        # Remove question words
        query = re.sub(r'(كيف|ما هي|ماهي|هل|أين|متى|لماذا)', '', query)
        query = re.sub(r'(أحصل|احصل|أتقدم|اتقدم|استخرج)', '', query)
        query = re.sub(r'(على|علي|من|في|إلى|الى)', '', query)
        query = re.sub(r'[؟?]', '', query)
        
        # Get remaining words
        words = query.split()
        keywords = [w for w in words if len(w) > 2]
        
        return keywords
    
    def create_enhanced_query(self, query: str) -> str:
        """Create enhanced query with keywords repeated"""
        keywords = self.extract_keywords(query)
        
        # Repeat important keywords
        enhanced = query + " " + " ".join(keywords)
        
        return enhanced
    
    def encode_multi_strategy(self, query: str) -> np.ndarray:
        """Encode query using multiple strategies"""
        # Strategy 1: Original query
        emb1 = self.model.encode([query])[0]
        
        # Strategy 2: Enhanced with keywords
        enhanced = self.create_enhanced_query(query)
        emb2 = self.model.encode([enhanced])[0]
        
        # Strategy 3: Synonym variations
        variations = self.expand_with_synonyms(query)
        if len(variations) > 1:
            emb3 = np.mean(self.model.encode(variations), axis=0)
        else:
            emb3 = emb1
        
        # Weighted average
        final_emb = (0.5 * emb1 + 0.3 * emb2 + 0.2 * emb3)
        
        return final_emb.astype('float32')


def test_improved_retrieval():
    """Test improved retrieval strategies"""
    
    print("="*80)
    print("IMPROVED RETRIEVAL TEST")
    print("="*80)
    
    # Load original system
    print("\nLoading system...")
    embeddings = np.load('index/embeddings.npy').astype('float32')
    faiss.normalize_L2(embeddings)
    
    with open('index/corpus_chunks.json', 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    with open('index/corpus_meta.json', 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Load test queries
    with open('experiments/test_queries_dataset.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    test_queries = dataset['queries'][:50]
    
    # Test strategies
    processor = SmartQueryProcessor()
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    strategies = {
        'baseline': [],
        'keyword_boost': [],
        'synonym_expansion': [],
        'multi_strategy': []
    }
    
    print("\nTesting strategies...")
    for test_query in test_queries:
        query = test_query['query_ar']
        expected = test_query['category']
        
        # Baseline
        emb = model.encode([query])[0].astype('float32').reshape(1, -1)
        faiss.normalize_L2(emb)
        sims = cosine_similarity(emb, embeddings)[0]
        top_cat = metadata[np.argmax(sims)]['category']
        strategies['baseline'].append(1 if top_cat == expected else 0)
        
        # Keyword boost
        enhanced = processor.create_enhanced_query(query)
        emb = model.encode([enhanced])[0].astype('float32').reshape(1, -1)
        faiss.normalize_L2(emb)
        sims = cosine_similarity(emb, embeddings)[0]
        top_cat = metadata[np.argmax(sims)]['category']
        strategies['keyword_boost'].append(1 if top_cat == expected else 0)
        
        # Synonym expansion
        variations = processor.expand_with_synonyms(query)
        emb = np.mean(model.encode(variations), axis=0).astype('float32').reshape(1, -1)
        faiss.normalize_L2(emb)
        sims = cosine_similarity(emb, embeddings)[0]
        top_cat = metadata[np.argmax(sims)]['category']
        strategies['synonym_expansion'].append(1 if top_cat == expected else 0)
        
        # Multi-strategy
        emb = processor.encode_multi_strategy(query).reshape(1, -1)
        faiss.normalize_L2(emb)
        sims = cosine_similarity(emb, embeddings)[0]
        top_cat = metadata[np.argmax(sims)]['category']
        strategies['multi_strategy'].append(1 if top_cat == expected else 0)
    
    # Results
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    
    for name, results in strategies.items():
        acc = sum(results) / len(results)
        correct = sum(results)
        print(f"{name:20s}: {acc:.1%} ({correct}/50)")
    
    best_strategy = max(strategies.items(), key=lambda x: sum(x[1]))
    print(f"\n[BEST] {best_strategy[0]}: {sum(best_strategy[1])/50:.1%}")
    
    return strategies


if __name__ == "__main__":
    results = test_improved_retrieval()
