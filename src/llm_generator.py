"""LLM-based answer generation using Google Gemini"""
import os
from google import generativeai as genai
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

class AnswerGenerator:
    """Generate answers using Google Gemini with automatic fallback"""
    
    def __init__(self, model_names: List[str] = None):
        """Initialize Gemini with multiple model fallbacks"""
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        
        # Default models to try in order (free tier models, newest first)
        if model_names is None:
            self.model_names = [
                "gemini-2.5-flash",          # Newest and fastest (WORKS)
                "gemini-2.5-flash-lite",     # Lighter version (WORKS)
                "gemini-flash-latest",       # Latest stable alias (WORKS)
                "gemini-flash-lite-latest"   # Lightest fallback (WORKS)
            ]
        else:
            self.model_names = model_names
        
        self.models = [genai.GenerativeModel(name) for name in self.model_names]
        print(f"✅ Gemini models initialized with fallback: {', '.join(self.model_names)}")
    
    def generate_answer(self, query: str, contexts: List[Dict], language: str = 'ar', return_language: str = 'ar') -> Dict:
        """
        Generate answer from retrieved contexts
        
        Args:
            query: User question
            contexts: List of retrieved chunks with metadata
            language: Input language ('ar' or 'en')
            return_language: Output language ('ar' or 'en')
        
        Returns:
            Dictionary with query, answer, and sources
        """
        # Prepare context string based on return language
        context_str = ""
        if return_language == 'ar':
            for i, ctx in enumerate(contexts[:3], 1):  # Top 3
                context_str += f"\n\n[مصدر {i}]\n{ctx['chunk']}\n"
                context_str += f"الفئة: {ctx['metadata']['category']}\n"
        else:
            for i, ctx in enumerate(contexts[:3], 1):  # Top 3
                context_str += f"\n\n[Source {i}]\n{ctx['chunk']}\n"
                context_str += f"Category: {ctx['metadata']['category']}\n"
        
        # Construct prompt based on return language
        if return_language == 'ar':
            prompt = f"""أنت مساعد ذكي متخصص في الإجابة على أسئلة حول الخدمات الحكومية في قطر.

استخدم المعلومات التالية للإجابة على السؤال. إذا لم تجد إجابة في المعلومات المقدمة، قل ذلك بوضوح.

المعلومات المتاحة:
{context_str}

السؤال: {query}

تعليمات:
1. أجب بالعربية الفصحى
2. كن دقيقاً ومختصراً
3. اذكر المصدر عند الحاجة (مثل: "حسب [مصدر 1]...")
4. إذا كانت المعلومات غير كافية، اذكر ذلك

الإجابة:"""
        
        else:  # English
            prompt = f"""You are an AI assistant specialized in answering questions about government services in Qatar.

Use the following information to answer the question. If you cannot find the answer in the provided information, say so clearly.

Available information:
{context_str}

Question: {query}

Instructions:
1. Answer in English
2. Be accurate and concise
3. Cite sources when needed (e.g., "According to [Source 1]...")
4. If information is insufficient, state that

Answer:"""
        
        # Call Gemini API with fallback
        answer = None
        last_error = None
        
        for i, model in enumerate(self.models):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.3,  # Lower = more factual
                        max_output_tokens=500
                    )
                )
                
                answer = response.text
                print(f"✅ Successfully used model: {self.model_names[i]}")
                break  # Success, exit loop
            
            except Exception as e:
                last_error = e
                print(f"⚠️ Model {self.model_names[i]} failed: {str(e)[:100]}")
                # Try next model
                continue
        
        # If all models failed
        if answer is None:
            if return_language == 'ar':
                answer = f"عذراً، حدث خطأ في توليد الإجابة: {str(last_error)}"
            else:
                answer = f"Sorry, an error occurred while generating the answer: {str(last_error)}"
        
        # Prepare full response
        result = {
            'query': query,
            'answer': answer,
            'sources': [
                {
                    'category': ctx['metadata']['category'],
                    'file': ctx['metadata']['source_file'],
                    'score': ctx['score']
                }
                for ctx in contexts[:3]
            ]
        }
        
        return result
