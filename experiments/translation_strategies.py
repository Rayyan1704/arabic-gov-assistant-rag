"""
Experiment 1: Translation Strategies Comparison
Tests 4 different approaches for handling English queries.

Research Question: Which translation strategy achieves best cross-lingual performance?
"""

import sys
import os
# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from translator import TranslationService
import faiss
from sklearn.metrics.pairwise import cosine_similarity
import time


class TranslationStrategyExperiment:
    """
    Compares 4 translation strategies:
    1. Direct English embeddings (no translation)
    2. Multilingual embeddings (current approach)
    3. Translation + Arabic embeddings (current approach)
    4. Back-translation for query expansion
    """
    
    def __init__(self):
        print("="*80)
        print("EXPERIMENT 1: TRANSLATION STRATEGIES")
        print("="*80)
        
        # Load data
        print("\nLoading data...")
        base_dir = os.path.join(os.path.dirname(__file__), '..')
        
        with open(os.path.join(base_dir, 'index', 'corpus_chunks.json'), 'r', encoding='utf-8') as f:
            self.chunks = json.load(f)
        
        with open(os.path.join(base_dir, 'index', 'corpus_meta.json'), 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
        
        # Load models
        print("Loading models...")
        self.ar_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        self.translator = TranslationService()
        
        # Generate Arabic embeddings (for methods 1 and 3)
        print("Generating Arabic embeddings...")
        self.ar_embeddings = self.ar_model.encode(self.chunks, show_progress_bar=True)
        faiss.normalize_L2(self.ar_embeddings.astype('float32'))
        
        print("✅ Setup complete\n")
    
    def method1_direct_english(self, query):
        """
        Method 1: Direct English embeddings (no translation)
        Embed English query directly and search Arabic corpus
        """
        start = time.time()
        
        # Embed English query directly
        query_emb = self.ar_model.encode([query])[0].astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_emb)
        
        # Search
        similarities = cosine_similarity(query_emb, self.ar_embeddings)[0]
        top_indices = np.argsort(similarities)[-5:][::-1]
        
        elapsed = time.time() - start
        
        return {
            'method': 'Direct English',
            'top_indices': top_indices.tolist(),
            'scores': similarities[top_indices].tolist(),
            'time': elapsed
        }
    
    def method2_multilingual(self, query):
        """
        Method 2: Multilingual embeddings
        Same as method 1 but explicitly using multilingual model
        """
        # Same as method 1 (our current model is multilingual)
        return self.method1_direct_english(query)
    
    def method3_translate_then_embed(self, query):
        """
        Method 3: Translation + Arabic embeddings (current approach)
        Translate English to Arabic, then embed
        """
        start = time.time()
        
        # Translate to Arabic
        arabic_query = self.translator.translate_to_arabic(query)
        
        # Embed Arabic query
        query_emb = self.ar_model.encode([arabic_query])[0].astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_emb)
        
        # Search
        similarities = cosine_similarity(query_emb, self.ar_embeddings)[0]
        top_indices = np.argsort(similarities)[-5:][::-1]
        
        elapsed = time.time() - start
        
        return {
            'method': 'Translate + Embed',
            'arabic_query': arabic_query,
            'top_indices': top_indices.tolist(),
            'scores': similarities[top_indices].tolist(),
            'time': elapsed
        }
    
    def method4_back_translation(self, query):
        """
        Method 4: Back-translation for query expansion
        EN → AR → EN → AR (creates multiple query variations)
        """
        start = time.time()
        
        # Original translation
        ar1 = self.translator.translate_to_arabic(query)
        
        # Back-translate
        en_back = self.translator.translate_to_english(ar1)
        
        # Translate again (variation)
        ar2 = self.translator.translate_to_arabic(en_back)
        
        # Embed both Arabic versions
        emb1 = self.ar_model.encode([ar1])[0]
        emb2 = self.ar_model.encode([ar2])[0]
        
        # Average embeddings (query expansion)
        query_emb = ((emb1 + emb2) / 2).astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_emb)
        
        # Search
        similarities = cosine_similarity(query_emb, self.ar_embeddings)[0]
        top_indices = np.argsort(similarities)[-5:][::-1]
        
        elapsed = time.time() - start
        
        return {
            'method': 'Back-translation',
            'arabic_query_1': ar1,
            'arabic_query_2': ar2,
            'top_indices': top_indices.tolist(),
            'scores': similarities[top_indices].tolist(),
            'time': elapsed
        }
    
    def evaluate_query(self, query, expected_category):
        """Evaluate all 4 methods on a single query"""
        results = {
            'query': query,
            'expected_category': expected_category,
            'methods': {}
        }
        
        # Test all methods
        for method_name, method_func in [
            ('method1_direct', self.method1_direct_english),
            ('method2_multilingual', self.method2_multilingual),
            ('method3_translate', self.method3_translate_then_embed),
            ('method4_backtrans', self.method4_back_translation)
        ]:
            result = method_func(query)
            
            # Check if top result matches expected category
            top_idx = result['top_indices'][0]
            top_category = self.metadata[top_idx]['category']
            correct = (top_category == expected_category)
            
            # Calculate metrics
            p_at_1 = 1 if correct else 0
            
            # Check top 3
            top3_categories = [self.metadata[idx]['category'] for idx in result['top_indices'][:3]]
            p_at_3 = 1 if expected_category in top3_categories else 0
            
            # MRR
            try:
                rank = top3_categories.index(expected_category) + 1
                mrr = 1.0 / rank
            except ValueError:
                mrr = 0.0
            
            results['methods'][method_name] = {
                **result,
                'top_category': top_category,
                'correct': correct,
                'p@1': p_at_1,
                'p@3': p_at_3,
                'mrr': mrr
            }
        
        return results
    
    def run_experiment(self, test_queries):
        """Run full experiment on test set"""
        print("\n" + "="*80)
        print("RUNNING EXPERIMENT")
        print("="*80)
        
        all_results = []
        
        for i, test in enumerate(test_queries, 1):
            print(f"\n[{i}/{len(test_queries)}] {test['query'][:50]}...")
            result = self.evaluate_query(test['query'], test['expected'])
            all_results.append(result)
        
        # Calculate aggregate metrics
        metrics_summary = self.calculate_summary(all_results)
        
        return {
            'detailed_results': all_results,
            'summary': metrics_summary
        }
    
    def calculate_summary(self, results):
        """Calculate aggregate metrics across all queries"""
        methods = ['method1_direct', 'method2_multilingual', 'method3_translate', 'method4_backtrans']
        summary = {}
        
        for method in methods:
            p1_scores = [r['methods'][method]['p@1'] for r in results]
            p3_scores = [r['methods'][method]['p@3'] for r in results]
            mrr_scores = [r['methods'][method]['mrr'] for r in results]
            times = [r['methods'][method]['time'] for r in results]
            
            summary[method] = {
                'P@1': np.mean(p1_scores),
                'P@3': np.mean(p3_scores),
                'MRR': np.mean(mrr_scores),
                'Avg_Time': np.mean(times),
                'Total_Correct': sum(p1_scores)
            }
        
        return summary


def main():
    # Initialize experiment
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    exp = TranslationStrategyExperiment()
    
    # Test queries (English only for this experiment)
    test_queries = [
        # Transportation
        {'query': 'How do I get a limousine license?', 'expected': 'transportation'},
        {'query': 'Fish transport permit requirements', 'expected': 'transportation'},
        {'query': 'Air cargo license application', 'expected': 'transportation'},
        
        # Education
        {'query': 'How to register for courses at Qatar University?', 'expected': 'education'},
        {'query': 'HBKU admission process', 'expected': 'education'},
        {'query': 'University transcript request', 'expected': 'education'},
        
        # Health
        {'query': 'How to request medical consultation?', 'expected': 'health'},
        {'query': 'Hamad Medical Corporation job application', 'expected': 'health'},
        {'query': 'Healthcare practitioner license', 'expected': 'health'},
        
        # Business
        {'query': 'How to submit tenders?', 'expected': 'business'},
        {'query': 'Tax registration process', 'expected': 'business'},
        {'query': 'Commercial license reactivation', 'expected': 'business'},
    ]
    
    # Run experiment
    results = exp.run_experiment(test_queries)
    
    # Display results
    print("\n" + "="*80)
    print("RESULTS SUMMARY")
    print("="*80)
    
    print("\n{:<25} {:>8} {:>8} {:>8} {:>10}".format(
        "Method", "P@1", "P@3", "MRR", "Time(s)"
    ))
    print("-"*80)
    
    for method, metrics in results['summary'].items():
        method_name = method.replace('method', 'Method ').replace('_', ' ').title()
        print("{:<25} {:>7.1%} {:>7.1%} {:>8.3f} {:>10.3f}".format(
            method_name,
            metrics['P@1'],
            metrics['P@3'],
            metrics['MRR'],
            metrics['Avg_Time']
        ))
    
    # Save results
    output_path = os.path.join(base_dir, 'index', 'experiment1_translation_strategies.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Results saved to experiment1_translation_strategies.json")
    
    # Conclusion
    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    
    best_method = max(results['summary'].items(), key=lambda x: x[1]['P@1'])
    print(f"\nBest Method: {best_method[0]}")
    print(f"P@1: {best_method[1]['P@1']:.1%}")
    print(f"P@3: {best_method[1]['P@3']:.1%}")
    print(f"MRR: {best_method[1]['MRR']:.3f}")


if __name__ == "__main__":
    main()
