"""
End-to-end test with reranked retrieval + LLM generation.
This is the complete Day 5 system in action.
"""

from src.category_retrieval import RerankedRetriever
from src.llm_generator import AnswerGenerator
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv


def main():
    print("="*80)
    print("DAY 5: RERANKED RAG SYSTEM - END-TO-END TEST")
    print("="*80)
    
    # Load environment
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env file")
        return
    
    # Initialize components
    print("\nInitializing system...")
    print("1. Loading embedding model...")
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    print("2. Loading reranked retriever...")
    retriever = RerankedRetriever(
        'index/embeddings.npy',
        'index/corpus_chunks.json',
        'index/corpus_meta.json'
    )
    
    print("3. Loading LLM generator...")
    generator = AnswerGenerator()
    
    print("\n✅ System ready!")
    
    # Test queries
    test_queries = [
        "كيف أحصل على بطاقة صحية في قطر؟",
        "ما هي إجراءات فتح شركة جديدة؟",
        "كيف أسجل أطفالي في المدرسة؟",
        "ما هي متطلبات الحصول على رخصة قيادة؟",
        "كيف أستأجر شقة في الدوحة؟"
    ]
    
    results = []
    
    for i, query in enumerate(test_queries, 1):
        print("\n" + "="*80)
        print(f"QUERY {i}/{len(test_queries)}")
        print("="*80)
        print(f"Q: {query}")
        
        # Detect category
        detected_cat = retriever.detect_category(query)
        print(f"\nDetected category: {detected_cat or 'None (global search)'}")
        
        # Get query embedding
        query_emb = model.encode([query])[0]
        
        # Retrieve with reranking
        print("\nRetrieving with reranking...")
        retrieved_docs = retriever.search_with_rerank(
            query, query_emb, 
            category=detected_cat,
            initial_k=20, 
            final_k=3
        )
        
        print(f"✅ Retrieved {len(retrieved_docs)} documents")
        print("\nTop 3 results:")
        for doc in retrieved_docs:
            print(f"  [{doc['rank']}] Rerank: {doc['rerank_score']:.3f} | Original: {doc['original_score']:.3f}")
            print(f"      Category: {doc['metadata']['category']}")
            print(f"      {doc['chunk'][:100]}...")
        
        # Generate answer
        print("\nGenerating answer with Gemini...")
        result = generator.generate_answer(query, retrieved_docs)
        answer = result['answer']
        
        print("\n" + "-"*80)
        print("ANSWER:")
        print("-"*80)
        print(answer)
        print("-"*80)
        
        # Store result
        results.append({
            'query': query,
            'detected_category': detected_cat,
            'retrieved_docs': len(retrieved_docs),
            'top_rerank_score': retrieved_docs[0]['rerank_score'],
            'answer': answer
        })
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    print(f"\nTotal queries tested: {len(test_queries)}")
    print(f"Category detection rate: {sum(1 for r in results if r['detected_category']) / len(results) * 100:.1f}%")
    print(f"Average top rerank score: {sum(r['top_rerank_score'] for r in results) / len(results):.3f}")
    
    print("\n✅ Day 5 system test complete!")
    print("\nKey improvements over Day 4:")
    print("  1. ✅ Per-category indexes for focused search")
    print("  2. ✅ Automatic category detection")
    print("  3. ✅ Cross-encoder reranking for better accuracy")
    print("  4. ✅ Two-stage retrieval (fast + accurate)")


if __name__ == "__main__":
    main()
