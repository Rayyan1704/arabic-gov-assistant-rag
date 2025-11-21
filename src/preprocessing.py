import re
import arabic_reshaper
from bidi.algorithm import get_display


def normalize_arabic(text):
    """
    Normalize Arabic text for consistent processing
    LIGHTER normalization to preserve distinctive features
    """
    # Remove diacritics (tashkeel)
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    
    # Normalize alef variants (lighter - keep some distinction)
    text = re.sub(r'[إأآ]', 'ا', text)
    
    # DON'T normalize yaa/taa marbuta - they're distinctive!
    # text = re.sub(r'ى', 'ي', text)  # REMOVED
    # text = re.sub(r'ة', 'ه', text)  # REMOVED
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Keep more characters - don't be too aggressive
    # Keep Arabic, digits, spaces, and common punctuation
    text = re.sub(r'[^\u0600-\u06FF\s\d\.\،\؛\؟\-\:]', '', text)
    
    return text.strip()


def clean_document(text):
    """
    Clean document text while preserving structure
    """
    # Remove multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove lines with only symbols
    lines = text.split('\n')
    lines = [l for l in lines if len(l.strip()) > 10]
    
    return '\n'.join(lines)


# Test it
if __name__ == "__main__":
    sample = "اَلسَّلامُ عَلَيْكُم"
    print(normalize_arabic(sample))
    # Should output: السلام عليكم
