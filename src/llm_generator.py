"""
LLM Answer Generator using Google Gemini
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


class AnswerGenerator:
    def __init__(self):
        """Initialize Gemini API"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Get your key from https://makersuite.google.com/app/apikey "
                "and add it to .env file"
            )
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_answer(self, query, contexts, language='ar'):
        """
        Generate answer from retrieved contexts
        
        Args:
            query: User question
            contexts: List of retrieved chunks with metadata
            language: 'ar' or 'en'
        
        Returns:
            dict with query, answer, and sources
        """
        # Prepare context string
        context_str = ""
        for i, ctx in enumerate(contexts[:3], 1):  # Top 3
            context_str += f"\n\n[مصدر {i}]\n{ctx['chunk']}\n"
            context_str += f"الفئة: {ctx['metadata']['category']}\n"
        
        # Construct prompt
        if language == 'ar':
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
5. قدم خطوات واضحة إذا كان السؤال عن إجراءات

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
5. Provide clear steps if the question is about procedures

Answer:"""
        
        # Call Gemini API
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,  # Lower = more factual
                max_output_tokens=500,
            )
        )
        
        answer = response.text
        
        # Prepare full response
        result = {
            'query': query,
            'answer': answer,
            'sources': [
                {
                    'category': ctx['metadata']['category'],
                    'file': ctx['metadata']['source_file'].split('/')[-1],
                    'score': ctx['score']
                }
                for ctx in contexts[:3]
            ]
        }
        
        return result
    
    def generate_answer_with_history(self, query, contexts, chat_history=None, language='ar'):
        """
        Generate answer with conversation history
        
        Args:
            query: User question
            contexts: List of retrieved chunks
            chat_history: List of previous (query, answer) tuples
            language: 'ar' or 'en'
        
        Returns:
            dict with query, answer, and sources
        """
        # Prepare context
        context_str = ""
        for i, ctx in enumerate(contexts[:3], 1):
            context_str += f"\n\n[مصدر {i}]\n{ctx['chunk']}\n"
        
        # Prepare history
        history_str = ""
        if chat_history:
            for prev_q, prev_a in chat_history[-3:]:  # Last 3 exchanges
                history_str += f"\nسؤال سابق: {prev_q}\nإجابة سابقة: {prev_a}\n"
        
        # Construct prompt with history
        if language == 'ar':
            prompt = f"""أنت مساعد ذكي متخصص في الخدمات الحكومية في قطر.

{history_str if history_str else ''}

المعلومات المتاحة:
{context_str}

السؤال الحالي: {query}

تعليمات:
1. أجب بالعربية الفصحى
2. استخدم السياق من المحادثة السابقة إذا كان ذا صلة
3. كن دقيقاً ومختصراً
4. اذكر المصدر عند الحاجة

الإجابة:"""
        else:
            prompt = f"""You are an AI assistant for Qatar government services.

{history_str if history_str else ''}

Available information:
{context_str}

Current question: {query}

Instructions:
1. Answer in English
2. Use context from previous conversation if relevant
3. Be accurate and concise
4. Cite sources when needed

Answer:"""
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=500,
            )
        )
        
        return {
            'query': query,
            'answer': response.text,
            'sources': [
                {
                    'category': ctx['metadata']['category'],
                    'file': ctx['metadata']['source_file'].split('/')[-1],
                    'score': ctx['score']
                }
                for ctx in contexts[:3]
            ]
        }
