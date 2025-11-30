# Phase 6: Web Interface Development

**Timeline:** Days 11-12 (8 hours)  
**Focus:** Streamlit Application Development  
**Status:** Complete

---

## Objectives

1. Create web-based user interface
2. Implement interactive query processing
3. Add visualization and result exploration
4. Deploy production-ready application

---

## Application Architecture

### Technology Stack
- **Framework:** Streamlit 1.28.1
- **Backend:** Existing RAG system
- **Deployment:** Local/cloud-ready

### Interface Structure
```
Main Page
├── Header (Title + Description)
├── Query Input (Text area)
├── Settings Sidebar
│   ├── Category detection toggle
│   └── Reranking toggle
├── Results Display
│   ├── Answer Tab
│   ├── Sources Tab
│   └── Details Tab
└── Example Queries
```

---

## Implementation

### Application Setup
**File:** `app.py`

```python
import streamlit as st
from sentence_transformers import SentenceTransformer
from src.category_retrieval import RerankedRetriever
from src.llm_generator import AnswerGenerator

# Page configuration
st.set_page_config(
    page_title="Arabic Government Services Assistant",
    page_icon="🏛️",
    layout="wide"
)

# Model caching
@st.cache_resource
def load_models():
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    retriever = RerankedRetriever(...)
    generator = AnswerGenerator()
    return model, retriever, generator
```

### Query Processing

```python
if query:
    with st.spinner("Processing query..."):
        # Generate embedding
        query_emb = model.encode([query])[0]
        
        # Retrieve with optional reranking
        if use_reranking:
            results = retriever.search_with_rerank(query, query_emb, final_k=3)
        else:
            results = retriever.search(query_emb, k=3)
        
        # Generate answer
        context = [r['chunk'] for r in results]
        answer = generator.generate_answer(query, context)
        
        # Display results
        display_results(answer, results)
```

---

## User Interface Features

### Query Input
- Multi-line text area
- Character count display
- Submit button
- Example queries (6 categories)

### Settings Sidebar
```python
with st.sidebar:
    st.header("Settings")
    use_category = st.checkbox("Enable category detection", value=True)
    use_reranking = st.checkbox("Enable reranking", value=True)
    
    st.header("System Info")
    st.metric("Documents", "51")
    st.metric("Categories", "8")
    st.metric("Accuracy", "96%")
```

### Results Display

**Answer Tab:**
```python
with tab1:
    st.markdown("### Answer")
    st.write(answer)
    
    # Confidence indicator
    avg_score = sum(r['score'] for r in results) / len(results)
    if avg_score > 0.7:
        st.success("High confidence answer")
    elif avg_score > 0.5:
        st.info("Good confidence answer")
    else:
        st.warning("Low confidence - answer may be incomplete")
```

**Sources Tab:**
```python
with tab2:
    st.markdown("### Retrieved Sources")
    for i, result in enumerate(results, 1):
        with st.expander(
            f"Source {i} - {result['metadata']['category']} "
            f"(Score: {result['score']:.3f})",
            expanded=(i == 1)
        ):
            st.json(result['metadata'])
            st.text_area("Content:", result['chunk'], height=200)
```

**Details Tab:**
```python
with tab3:
    st.markdown("### Query Details")
    st.write(f"**Detected Category:** {detected_category or 'None'}")
    st.write(f"**Reranking:** {'Enabled' if use_reranking else 'Disabled'}")
    st.write(f"**Results Retrieved:** {len(results)}")
```

### Example Queries

```python
st.markdown("### Try these examples:")
examples = [
    "كيف أحصل على رخصة قيادة؟",
    "How to register for university?",
    "ما هي خطوات تجديد جواز السفر؟",
    "Business license requirements",
    "كيف أحصل على بطاقة صحية؟",
    "Housing allowance eligibility"
]

cols = st.columns(3)
for i, example in enumerate(examples):
    with cols[i % 3]:
        if st.button(example, key=f"ex_{i}"):
            st.session_state.query = example
            st.rerun()
```

---

## Performance Optimization

### Model Caching
```python
@st.cache_resource
def load_models():
    # Load models once, reuse across sessions
    return model, retriever, generator
```

**Impact:**
- First load: 8.1s
- Subsequent queries: 0.1s (cached)

### Session State Management
```python
# Initialize session state
if 'query_history' not in st.session_state:
    st.session_state.query_history = []

if 'current_results' not in st.session_state:
    st.session_state.current_results = None
```

---

## Deployment Configuration

### Streamlit Config
**File:** `.streamlit/config.toml`

```toml
[server]
port = 8501
headless = true

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### Environment Variables
```bash
# .env file
GEMINI_API_KEY=your_gemini_key
```

---

## Testing Results

### Functionality Testing
- Query processing: Working
- Category detection: Working
- Reranking toggle: Working
- Answer generation: Working
- Source display: Working

### Performance Testing
| Component | Time (seconds) |
|-----------|----------------|
| App startup | 3.2 |
| Model loading (first time) | 8.1 |
| Model loading (cached) | 0.1 |
| Query processing | 1.0-3.0 |
| UI rendering | 0.5 |

### Browser Compatibility
- Chrome: Tested, working
- Firefox: Tested, working
- Safari: Compatible
- Edge: Compatible

---

## User Experience

### Workflow
1. User enters query (Arabic or English)
2. System detects category (if enabled)
3. System retrieves relevant documents
4. System applies reranking (if enabled)
5. System generates answer
6. User views answer and sources
7. User explores source documents

### Interaction Features
- Real-time processing feedback
- Expandable source documents
- Confidence indicators
- Example queries for guidance
- Settings customization

---

## Components Implemented

### Core Files
- `app.py` - Streamlit application
- `.streamlit/config.toml` - Configuration

### Dependencies
```
streamlit==1.28.1
```

---

## Deployment

### Local Deployment
```bash
streamlit run app.py
```

**Access:** http://localhost:8501

### Cloud Deployment Options
1. **Streamlit Cloud:** Direct GitHub integration
2. **Docker:** Containerized deployment
3. **Cloud platforms:** AWS, GCP, Azure

---

## Key Features

### Implemented
- Interactive query interface
- Real-time processing
- Source exploration
- Settings customization
- Example queries
- Confidence indicators
- Model caching

### User Benefits
- Easy to use: No technical knowledge required
- Fast: Cached models, optimized processing
- Transparent: Shows sources and confidence
- Flexible: Configurable settings
- Accessible: Web-based, no installation

---

## Challenges and Solutions

### Challenge 1: Model Loading Time
**Issue:** 8-second delay on first query  
**Cause:** Loading embedding model on demand  
**Solution:** Implemented @st.cache_resource for model persistence

### Challenge 2: Session State Management
**Issue:** Query results lost on page refresh  
**Cause:** Streamlit reruns script on interaction  
**Solution:** Used st.session_state to persist data across reruns

### Challenge 3: Arabic Text Display
**Issue:** Arabic text alignment issues in UI  
**Cause:** Default LTR (left-to-right) layout  
**Solution:** Added RTL CSS styling for Arabic content

### Challenge 4: Example Query Integration
**Issue:** Clicking example didn't populate input field  
**Cause:** Button click not updating text area  
**Solution:** Used session state + st.rerun() to update input

### Challenge 5: Source Document Display
**Issue:** Long documents made UI cluttered  
**Cause:** Displaying full text in results  
**Solution:** Implemented expandable sections with st.expander()

### Challenge 6: Confidence Indicator Logic
**Issue:** Uncertain threshold for confidence levels  
**Cause:** No established standards  
**Solution:** Tested with queries, set thresholds: >0.7 high, >0.5 good, <0.5 low

---

## Time Breakdown

- Streamlit learning: 2 hours
- Basic UI implementation: 2 hours
- Feature additions: 2 hours
- Styling and UX: 1.5 hours
- Testing and refinement: 0.5 hours

**Total:** 8 hours (Days 11-12)

---

## Next Phase

Phase 7: Translation integration and system enhancement (Days 13-14)
