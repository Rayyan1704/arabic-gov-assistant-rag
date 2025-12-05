"""
Translation Service for Bilingual RAG System
Handles Arabic-English translation for queries and answers.
"""

from deep_translator import GoogleTranslator
import re


class TranslationService:
    """
    Handles translation between Arabic and English.
    Uses Google Translate API (free tier).
    """
    
    def __init__(self):
        """Initialize translator"""
        # deep-translator doesn't need initialization
        print("[OK] Translation service initialized")
    
    def detect_language(self, text):
        """
        Detect if text is Arabic or English.
        
        Args:
            text: Input text
            
        Returns:
            'ar' for Arabic, 'en' for English
        """
        # Simple heuristic: check for Arabic characters
        arabic_pattern = re.compile(r'[\u0600-\u06FF]')
        
        if arabic_pattern.search(text):
            return 'ar'
        else:
            return 'en'
    
    def translate_to_arabic(self, text):
        """
        Translate English text to Arabic.
        
        Args:
            text: English text
            
        Returns:
            Arabic translation
        """
        try:
            result = GoogleTranslator(source='en', target='ar').translate(text)
            return result
        except Exception as e:
            print(f"⚠️ Translation error: {e}")
            return text  # Return original if translation fails
    
    def translate_to_english(self, text):
        """
        Translate Arabic text to English.
        
        Args:
            text: Arabic text
            
        Returns:
            English translation
        """
        try:
            result = GoogleTranslator(source='ar', target='en').translate(text)
            return result
        except Exception as e:
            print(f"⚠️ Translation error: {e}")
            return text  # Return original if translation fails
    
    def process_query(self, query):
        """
        Process a query: detect language and translate if needed.
        
        Args:
            query: User query in any language
            
        Returns:
            Dictionary with:
                - query_language: 'ar' or 'en'
                - arabic_query: Query in Arabic
                - needs_translation: Boolean
                - original_query: Original query
        """
        query_lang = self.detect_language(query)
        
        if query_lang == 'en':
            # Translate to Arabic for search
            arabic_query = self.translate_to_arabic(query)
            needs_translation = True
        else:
            # Already Arabic
            arabic_query = query
            needs_translation = False
        
        return {
            'query_language': query_lang,
            'arabic_query': arabic_query,
            'needs_translation': needs_translation,
            'original_query': query
        }
    
    def translate_answer(self, answer, target_language):
        """
        Translate answer to target language.
        
        Args:
            answer: Answer text
            target_language: 'ar' or 'en'
            
        Returns:
            Translated answer
        """
        answer_lang = self.detect_language(answer)
        
        # If already in target language, return as-is
        if answer_lang == target_language:
            return answer
        
        # Translate
        if target_language == 'en':
            return self.translate_to_english(answer)
        else:
            return self.translate_to_arabic(answer)
    
    def translate_text(self, text, target_lang):
        """
        Generic text translation method.
        
        Args:
            text: Text to translate
            target_lang: Target language ('ar' or 'en')
            
        Returns:
            Translated text
        """
        source_lang = self.detect_language(text)
        
        # If already in target language, return as-is
        if source_lang == target_lang:
            return text
        
        # Translate
        if target_lang == 'en':
            return self.translate_to_english(text)
        else:
            return self.translate_to_arabic(text)
