"""LLM-based answer generation using Google Gemini"""
import os
from google import generativeai as genai
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

class AnswerGenerator:
    """Generate answers using Google Gemini"""
    
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """Initialize Gemini model"""
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        print(f"✅ Gemini model initialized: {model_name}")
    
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
        
        # Call Gemini API
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,  # Lower = more factual
                    max_output_tokens=500
                )
            )
            
            answer = response.text
        
        except Exception as e:
            if return_language == 'ar':
                answer = f"عذراً، حدث خطأ في توليد الإجابة: {str(e)}"
            else:
                answer = f"Sorry, an error occurred while generating the answer: {str(e)}"
        
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
