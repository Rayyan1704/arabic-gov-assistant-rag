"""Text preprocessing utilities for Arabic documents"""
import re
from pathlib import Path
from typing import List, Dict

class ArabicPreprocessor:
    """Handles Arabic text preprocessing"""
    
    def __init__(self):
        pass
    
    def normalize_arabic(self, text: str) -> str:
        """Normalize Arabic text for better retrieval"""
        if not text:
            return ""
        
        # Remove diacritics (tashkeel)
        text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
        
        # Normalize alef variants (إ، أ، آ → ا)
        text = re.sub(r'[إأآ]', 'ا', text)
        
        # Normalize taa marbuta and haa
        # text = re.sub(r'ة', 'ه', text)  # Optional
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Keep Arabic, digits, spaces, and common punctuation
        text = re.sub(r'[^\u0600-\u06FF\s\d\.\،\؛\؟\-\:]', '', text)
        
        return text.strip()
    
    def clean_document(self, text: str) -> str:
        """Clean document text while preserving structure"""
        if not text:
            return ""
        
        # Remove excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove lines that are too short (likely noise)
        lines = text.split('\n')
        lines = [line for line in lines if len(line.strip()) > 10]
        
        return '\n'.join(lines)
    
    def load_document(self, filepath: Path) -> str:
        """Load document from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return ""
    
    def get_category_from_path(self, filepath: Path) -> str:
        """Extract category from file path"""
        parts = str(filepath).replace('\\', '/').split('/')
        if 'data' in parts:
            data_idx = parts.index('data')
            if data_idx + 1 < len(parts):
                return parts[data_idx + 1]
        return 'unknown'
    
    def load_all_documents(self, data_dir: Path) -> List[Dict]:
        """Load all documents from data directory"""
        documents = []
        
        for category_dir in sorted(data_dir.iterdir()):
            if not category_dir.is_dir() or category_dir.name == 'archive_backup':
                continue
            
            category = category_dir.name
            
            for filepath in category_dir.glob("*.txt"):
                text = self.load_document(filepath)
                if text:
                    documents.append({
                        'text': text,
                        'category': category,
                        'filename': filepath.name,
                        'filepath': str(filepath)
                    })
        
        return documents
