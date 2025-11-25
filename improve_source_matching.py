"""
Improve source-level matching
Goal: "driving license" query → driving license document (not just transportation category)
"""

import sys
import os
sys.path.insert(0, 'src')

import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from sklearn.metrics.pairwise import cosine_similarity
from translator import TranslationService
import re


class EnhancedRetriever:
    """Retriever with title matching and keyword boosting"""
    
    def __init__(self):
        # Load system
        self.embeddings = np.load('index/embeddings.npy').astype('float32')
        faiss.normalize_L2(self.embeddings)
        
        with open('index/corpus_chunks.json', 'r', encoding='utf-8') as f:
            self.chunks = json.load(f)
        
        with open('index/corpus_meta.json', 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
        
        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        
        # Extract titles from chunks
        self.titles = self._extract_titles()
        
        # Build keyword to document mapping
        self.keyword_to_doc = self._build_keyword_map()
    
    def _extract_titles(self):
        """Extract service titles from chunks"""
        titles = []
        for chunk in self.chunks:
            lines = chunk.split('\n')
            title = lines[0] if lines else ""
            titles.append(title.strip())
        return titles
    
    def _build_keyword_map(self):
        """Map keywords to specific document indices"""
        keyword_map = {}
        
        for idx, (title, meta) in enumerate(zip(self.titles, self.metadata)):
            title_lower = title.lower()
            
            # Extract key terms from title
            keywords = []
            
            # Driving license
            if 'قياده' in title or 'سواقه' in title or 'driving' in title_lower:
                keywords.extend(['رخصة قيادة', 'رخصة سواقة', 'driving license', 'سواقة', 'قيادة'])
            
            # Limousine
            if 'ليموزين' in title or 'limousine' in title_lower or 'limo' in title_lower:
                keywords.extend(['ليموزين', 'limousine', 'limo', 'تاجير سيارات'])
            
            # School registration
            if 'تسجيل' in title and 'مدرس' in title:
                keywords.extend(['تسجيل مدرسة', 'school registration', 'register school'])
            
            # University
            if 'جامعه' in title or 'university' in title_lower:
                keywords.extend(['جامعة', 'university', 'جامعه قطر'])
            
            # Transcript
            if 'كشف' in title and 'درجات' in title:
                keywords.extend(['كشف درجات', 'transcript', 'كشف الدرجات'])
            
            # Doctor
            if 'دكتور' in title or 'طبيب' in title or 'doctor' in title_lower:
                keywords.extend(['دكتور', 'طبيب', 'doctor', 'بحث طبيب'])
            
            # Nurse
            if 'ممرض' in title or 'nurse' in title_lower:
                keywords.extend(['ممرض', 'nurse', 'ممرضة'])
            
            # Business license
            if 'تجاري' in title and 'رخص' in title:
                keywords.extend(['رخصة تجارية', 'business license', 'تجارية'])
            
            # Tenders
            if 'مناقص' in title or 'tender' in title_lower:
                keywords.extend(['مناقصات', 'tenders', 'مناقصة'])
            
            # Rent allowance
            if 'بدل' in title and 'ايجار' in title:
                keywords.extend(['بدل ايجار', 'rent allowance', 'بدل إيجار'])
            
            # Hukoomi
            if 'حكومي' in title or 'hukoomi' in title_lower:
                keywords.extend(['حكومي', 'hukoomi', 'بوابة حكومي'])
            
            # Court/Justice
            if 'قضي' in title or 'محكم' in title or 'court' in title_lower:
                keywords.extend(['قضية', 'محكمة', 'court case'])
            
            # Radio license
            if 'راديو' in title or 'radio' in title_lower:
                keywords.extend(['راديو', 'radio', 'ترخيص راديو'])
            
            # Map keywords to this document
            for keyword in keywords:
                if keyword not in keyword_map:
                    keyword_map[keyword] = []
                keyword_map[keyword].append(idx)
        
        return keyword_map
    
    def _title_similarity(self, query: str, title: str) -> float:
        """Calculate title similarity score"""
        query_lower = query.lower()
        title_lower = title.lower()
        
        # Exact match
        if query_lower in title_lower or title_lower in query_lower:
            return 1.0
        
        # Word overlap
        query_words = set(query_lower.split())
        title_words = set(title_lower.split())
        
        if not query_words or not title_words:
            return 0.0
        
        overlap = len(query_words & title_words)
        return overlap / max(len(query_words), len(title_words))
    
    def search_enhanced(self, query: str, k: int = 10):
        """Enhanced search with title matching"""
        
        # 1. Semantic search
        query_emb = self.model.encode([query])[0].astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_emb)
        semantic_scores = cosine_similarity(query_emb, self.embeddings)[0]
        
        # 2. Title matching scores
        title_scores = np.array([
            self._title_similarity(query, title) 
            for title in self.titles
        ])
        
        # 3. Keyword boosting
        keyword_scores = np.zeros(len(self.chunks))
        query_lower = query.lower()
        
        for keyword, doc_indices in self.keyword_to_doc.items():
            if keyword in query_lower:
                for idx in doc_indices:
                    keyword_scores[idx] = 1.0
        
        # 4. Combined scoring
        # Title match is VERY important (50%)
        # Semantic is important (40%)
        # Keyword boost (10%)
        final_scores = (
            0.50 * title_scores +
            0.40 * semantic_scores +
            0.10 * keyword_scores
        )
        
        # Get top k
        top_indices = np.argsort(final_scores)[-k:][::-1]
        
        results = []
        for rank, idx in enumerate(top_indices, 1):
            results.append({
                'rank': rank,
                'index': int(idx),
                'score': float(final_scores[idx]),
                'semantic_score': float(semantic_scores[idx]),
                'title_score': float(title_scores[idx]),
                'keyword_score': float(keyword_scores[idx]),
                'category': self.metadata[idx]['category'],
                'source': self.metadata[idx]['source_file'],
                'title': self.titles[idx],
                'chunk': self.chunks[idx][:200]
            })
        
        return results


def test_source_matching():
    """Test if queries match correct sources"""
    
    print("="*80)
    print("SOURCE-LEVEL MATCHING TEST")
    print("="*80)
    
    retriever = EnhancedRetriever()
    translator = TranslationService()
    
    # Test cases with expected source files
    test_cases = [
        # Transportation
        {'query': 'driving license', 'expected_source': 'transportation_moi_driving_license.txt'},
        {'query': 'رخصة قيادة', 'expected_source': 'transportation_moi_driving_license.txt'},
        {'query': 'رخصة سواقة', 'expected_source': 'transportation_moi_driving_license.txt'},
        {'query': 'limousine license', 'expected_source': 'transportation_mot_limo_license.txt'},
        {'query': 'ليموزين', 'expected_source': 'transportation_mot_limo_license.txt'},
        
        # Education
        {'query': 'school registration', 'expected_source': 'education_moehe_no_vacancy_registration.txt'},
        {'query': 'تسجيل مدرسة', 'expected_source': 'education_moehe_no_vacancy_registration.txt'},
        {'query': 'transcript', 'expected_source': 'education_qu_transcript_request.txt'},
        {'query': 'كشف درجات', 'expected_source': 'education_qu_transcript_request.txt'},
        {'query': 'university admission', 'expected_source': 'education_hbku_admission_application.txt'},
        
        # Health
        {'query': 'find doctor', 'expected_source': 'health_moph_doctor_search.txt'},
        {'query': 'بحث عن دكتور', 'expected_source': 'health_moph_doctor_search.txt'},
        {'query': 'nurse search', 'expected_source': 'health_moph_nurse_search.txt'},
        {'query': 'بحث ممرض', 'expected_source': 'health_moph_nurse_search.txt'},
        
        # Business
        {'query': 'business license', 'expected_source': 'business_moci_license_reactivation.txt'},
        {'query': 'رخصة تجارية', 'expected_source': 'business_moci_license_reactivation.txt'},
        {'query': 'tenders', 'expected_source': 'business_caa_tenders_submission.txt'},
        {'query': 'مناقصات', 'expected_source': 'business_caa_tenders_submission.txt'},
        
        # Housing
        {'query': 'rent allowance', 'expected_source': 'housing_mm_rent_allowance.txt'},
        {'query': 'بدل ايجار', 'expected_source': 'housing_mm_rent_allowance.txt'},
        
        # Info
        {'query': 'hukoomi', 'expected_source': 'about_hukoomi.txt'},
        {'query': 'حكومي', 'expected_source': 'about_hukoomi.txt'},
    ]
    
    print(f"\nTesting {len(test_cases)} source-level matches...\n")
    
    correct = 0
    results = []
    
    for i, test in enumerate(test_cases, 1):
        query = test['query']
        expected_source = test['expected_source']
        
        # Translate if English
        is_english = any(c.isascii() and c.isalpha() for c in query)
        if is_english:
            query_to_search = translator.translate_to_arabic(query)
            lang = "EN"
        else:
            query_to_search = query
            lang = "AR"
        
        # Search
        search_results = retriever.search_enhanced(query_to_search, k=5)
        
        # Check if top result matches expected source
        top_source = search_results[0]['source'].split('\\')[-1]
        is_correct = top_source == expected_source
        
        if is_correct:
            correct += 1
            status = "✓"
        else:
            status = "✗"
        
        results.append({
            'query': query,
            'lang': lang,
            'expected': expected_source,
            'got': top_source,
            'correct': is_correct,
            'score': search_results[0]['score']
        })
        
        print(f"[{i:2d}] {status} {lang} | {query:25s}")
        print(f"     Expected: {expected_source}")
        print(f"     Got:      {top_source}")
        if not is_correct:
            print(f"     Top 3: {[r['source'].split('\\\\')[-1] for r in search_results[:3]]}")
        print()
    
    # Summary
    accuracy = correct / len(test_cases)
    
    print("="*80)
    print("RESULTS")
    print("="*80)
    print(f"\nSource-Level Accuracy: {accuracy:.1%} ({correct}/{len(test_cases)})")
    
    # By language
    en_results = [r for r in results if r['lang'] == 'EN']
    ar_results = [r for r in results if r['lang'] == 'AR']
    
    en_correct = sum(1 for r in en_results if r['correct'])
    ar_correct = sum(1 for r in ar_results if r['correct'])
    
    print(f"\nEnglish: {en_correct}/{len(en_results)} ({en_correct/len(en_results):.1%})")
    print(f"Arabic:  {ar_correct}/{len(ar_results)} ({ar_correct/len(ar_results):.1%})")
    
    # Failures
    failures = [r for r in results if not r['correct']]
    if failures:
        print(f"\nFailures ({len(failures)}):")
        for fail in failures:
            print(f"  '{fail['query']}' → Expected: {fail['expected']}, Got: {fail['got']}")
    
    if accuracy >= 0.90:
        print(f"\n🏆 EXCELLENT: Source matching is highly accurate!")
    elif accuracy >= 0.80:
        print(f"\n✓ GOOD: Source matching works well")
    else:
        print(f"\n⚠️  NEEDS IMPROVEMENT: Source matching needs work")
    
    return {
        'accuracy': accuracy,
        'correct': correct,
        'total': len(test_cases),
        'results': results
    }


if __name__ == "__main__":
    results = test_source_matching()
