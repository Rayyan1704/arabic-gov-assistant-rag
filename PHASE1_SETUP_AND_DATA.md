# Phase 1: Project Setup and Data Collection

**Timeline:** Days 1-2 (8 hours)  
**Focus:** Environment Setup, Data Collection, and Initial Architecture  
**Status:** Complete

---

## Objectives

1. Configure development environment
2. Collect government service documents
3. Establish project structure
4. Implement Arabic text preprocessing
5. Develop document chunking system

---

## Environment Setup

### Configuration
- Python 3.12 environment
- Virtual environment created
- Dependencies installed (see requirements.txt)
- Google Gemini API configured
- Google Translate API configured

### Project Structure
```
Root/
├── src/
│   ├── preprocessing.py
│   ├── chunking.py
│   ├── retrieval.py
│   └── llm_generator.py
├── data/
│   ├── business/
│   ├── culture/
│   ├── education/
│   ├── health/
│   ├── housing/
│   ├── info/
│   ├── justice/
│   └── transportation/
├── index/
├── notebooks/
└── requirements.txt
```

---

## Data Collection

### Corpus Statistics
- Total documents: 50
- Categories: 8
- Format: Plain text (.txt)
- Language: Arabic
- Source: Qatar Government Services

### Category Distribution
| Category | Documents | Topics |
|----------|-----------|--------|
| Transportation | 8 | Driving licenses, vehicle registration, permits |
| Education | 8 | University services, school registration, transcripts |
| Health | 8 | Medical services, doctor search, health permits |
| Business | 7 | Commercial licenses, permits, registrations |
| Housing | 6 | Housing services, rent allowances, property |
| Culture | 5 | Cultural events, permits, activities |
| Info | 5 | Government information, contact details |
| Justice | 4 | Legal services, court procedures |

---

## Text Preprocessing

### Implementation
**File:** `src/preprocessing.py`

**Functions:**
```python
def normalize_arabic(text):
    # Remove diacritics
    # Normalize Arabic variants (ا، أ، إ، آ → ا)
    # Normalize Taa Marbuta (ة → ه)
    # Remove Tatweel (ـ)
    return normalized_text

def clean_document(text):
    # Apply normalization
    # Remove extra whitespace
    # Preserve paragraph structure
    return cleaned_text
```

**Normalization Rules:**
- Diacritics removed (َ ُ ِ ّ ْ)
- Alef variants normalized (أ، إ، آ → ا)
- Taa Marbuta normalized (ة → ه)
- Tatweel removed (ـ)
- Extra whitespace collapsed

---

## Document Chunking

### Implementation
**File:** `src/chunking.py`

**Strategy:** Paragraph-based chunking with overlap

**Parameters:**
```python
chunk_size = 512        # Maximum characters per chunk
overlap = 128           # Overlap between chunks
min_chunk_size = 412    # Minimum chunk size (80% of chunk_size)
```

**Process:**
```python
def chunk_by_paragraph(text, chunk_size=512, overlap=128):
    # Split by paragraphs
    # Combine paragraphs into chunks
    # Apply overlap between chunks
    # Filter by minimum size
    return chunks
```

---

## Document Processing

### Execution
**Script:** `process_all_documents.py`

**Results:**
- Documents processed: 50
- Chunks created: 50
- Output: `index/corpus_chunks.json`
- Metadata: `index/corpus_meta.json`

### Metadata Structure
```json
{
  "chunk_id": 0,
  "source_file": "business/business_license.txt",
  "category": "business",
  "title": "Business License Application",
  "chunk_index": 0,
  "total_chunks": 1
}
```

---

## Data Quality Verification

### Validation
**Script:** `verify_data.py`

**Checks:**
- File existence
- File readability
- Text encoding (UTF-8)
- Minimum content length
- Category distribution

**Results:**
- Files verified: 50
- Issues found: 0
- All files valid

---

## Components Implemented

### Source Files
- `src/preprocessing.py` - Arabic text normalization
- `src/chunking.py` - Document chunking
- `process_all_documents.py` - Batch processing
- `verify_data.py` - Data validation

### Dependencies
```
python-dotenv==1.0.0
google-generativeai==0.3.2
googletrans==4.0.0rc1
```

---

## Technical Details

### Text Encoding
- Input: UTF-8
- Output: UTF-8
- Arabic text handling: Native Python 3 Unicode support

### Chunking Rationale
- Paragraph-based: Preserves semantic coherence
- 512 characters: Balances context and specificity
- 128 overlap: Prevents information loss at boundaries
- 412 minimum: Ensures sufficient context

---

## Challenges and Solutions

### Challenge 1: Arabic Text Encoding
**Issue:** Initial file reading errors with Arabic text  
**Cause:** Default encoding (cp1252) incompatible with Arabic characters  
**Solution:** Explicitly specified UTF-8 encoding in all file operations

```python
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
```

### Challenge 2: Inconsistent Document Structure
**Issue:** Documents had varying formats (headers, footers, metadata)  
**Cause:** Manual document collection from different sources  
**Solution:** Implemented standardized preprocessing pipeline to normalize structure

### Challenge 3: Chunking Strategy Selection
**Issue:** Uncertain optimal chunk size for Arabic government documents  
**Cause:** No established best practices for this domain  
**Solution:** Implemented configurable chunking with 512/128 as starting point, planned experiments for Phase 4

### Challenge 4: Category Organization
**Issue:** Some documents fit multiple categories  
**Cause:** Overlapping government service domains  
**Solution:** Assigned primary category based on main service focus, documented in metadata

---

## Time Breakdown

- Environment setup: 2 hours
- Data collection: 3 hours
- Project structure: 1 hour
- Preprocessing implementation: 1.5 hours
- Chunking implementation: 2 hours
- Testing and validation: 0.5 hours

**Total:** 8 hours (Days 1-2)

---

## Next Phase

Phase 2: Core system development with embeddings and FAISS indexing (Days 3-4)
