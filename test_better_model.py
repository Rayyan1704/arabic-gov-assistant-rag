"""
Test with better embedding models
"""

import sys
import os
sys.path.insert(0, 'src')

import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from sklearn.metrics.pairwise import cosine_similarity


def test_model(model_name: str):
    """Test a specific model"""
    
    print(f"\nTesting: {model_name}")
    print("-" * 60)
    
    try:
        # Load model
        model = SentenceTransformer(model_name)
        
        # Load data
        with open('index/corpus_chunks.json', 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        
        with open('index/corpus_meta.json', 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = model.encode(chunks, show_progress_bar=True)
        embeddings = embeddings.astype('float32')
        faiss.normalize_L2(embeddings)
        
        # Load test queries
        with open('experiments/test_queries_dataset.json', 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        
        test_queries = dataset['queries'][:50]
        
        # Test
        correct = 0
        for test_query in test_queries:
            query = test_query['query_ar']
            expected = test_query['category']
            
            query_emb = model.encode([query])[0].astype('float32').reshape(1, -1)
            faiss.normalize_L2(query_emb)
            
            sims = cosine_similarity(query_emb, embeddings)[0]
            top_idx = np.argmax(sims)
            top_cat = metadata[top_idx]['category']
            
            if top_cat == expected:
                correct += 1
        
        accuracy = correct / len(test_queries)
        print(f"Accuracy: {accuracy:.1%} ({correct}/{len(test_queries)})")
        
        return accuracy
        
    except Exception as e:
        print(f"Error: {e}")
        return 0.0


def main():
    """Test multiple models"""
    
    print("="*80)
    print("EMBEDDING MODEL COMPARISON")
    print("="*80)
    
    models = [
        ('paraphrase-multilingual-mpnet-base-v2', 'Current model'),
        ('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', 'Faster alternative'),
        ('intfloat/multilingual-e5-base', 'E5 base (better Arabic)'),
    ]
    
    results = {}
    
    for model_name, description in models:
        print(f"\n{description}")
        acc = test_model(model_name)
        results[model_name] = acc
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    for model_name, acc in results.items():
        print(f"{model_name:50s}: {acc:.1%}")
    
    best = max(results.items(), key=lambda x: x[1])
    print(f"\n[BEST] {best[0]}: {best[1]:.1%}")


if __name__ == "__main__":
    main()
