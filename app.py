"""
AraGovAssist - Streamlit Demo UI
Interactive web interface for the Qatar Government Services RAG system.
"""

import streamlit as st
import sys
import time
sys.path.append('src')

from sentence_transformers import SentenceTransformer
from retrieval import RetrieverSystem
from llm_generator import AnswerGenerator
from translator import TranslationService

# Page config
st.set_page_config(
    page_title="AraGovAssist - Qatar Gov Services",
    page_icon="🇶🇦",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #8E1538 0%, #C41E3A 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🇶🇦 AraGovAssist</h1>
    <p>مساعد الخدمات الحكومية القطرية الذكي</p>
    <p><i>Qatar Government Services Intelligent Assistant</i></p>
</div>
""", unsafe_allow_html=True)

# Load models (cache for performance)
@st.cache_resource
def load_models(_force_reload=False):
    """Load and cache all models"""
    with st.spinner("🔄 Loading AI models..."):
        model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        
        retriever = RetrieverSystem(
            'index/embeddings.npy',
            'index/corpus_chunks.json',
            'index/corpus_meta.json'
        )
        
        generator = AnswerGenerator()
        translator = TranslationService()
        
        return model, retriever, generator, translator

try:
    # Force reload if needed (change this value to bust cache)
    model, retriever, generator, translator = load_models(_force_reload=True)
    st.success("✅ System ready! Ask your question below.")
except Exception as e:
    st.error(f"❌ Error loading models: {str(e)}")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # About section first
    st.markdown("### 📖 About")
    st.markdown("""
    **AraGovAssist** is a bilingual RAG system for Qatar government services.
    
    **Features:**
    - 🔍 Semantic search
    - 🎯 Category detection
    - 🤖 AI-powered answers
    - 🌐 Bilingual support
    - 📄 Full document access
    
    **Tech Stack:**
    - FAISS vector search
    - Multilingual embeddings
    - Google Gemini LLM
    - Streamlit UI
    """)
    
    st.markdown("---")
    
    # Number of sources
    num_results = st.slider("Number of sources", 1, 10, 3,
                           help="How many source documents to retrieve")
    
    st.markdown("---")
    
    # Language Settings
    st.markdown("### 🌐 Language Settings")
    answer_lang = st.radio(
        "Answer language:",
        ["Same as query", "Always Arabic", "Always English"],
        index=0,
        help="Choose output language for answers and sources"
    )
    
    st.markdown("---")
    
    # System stats
    st.markdown("### 📊 Formal Queries")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Category", "99%")
    with col2:
        st.metric("Source", "84%")
    
    st.markdown("### 📊 Messy Queries")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Category", "84%")
    with col2:
        st.metric("Source", "51%")
    
    st.markdown("---")
    st.markdown("### ⚡ System")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Documents", "51")
    with col2:
        st.metric("Response", "<1s")

# Initialize session state for query if not exists
if 'current_query' not in st.session_state:
    st.session_state.current_query = ""

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Ask Your Question")
    
    # Use form to prevent rerun issues
    with st.form(key="query_form"):
        query = st.text_area(
            "Enter your question in Arabic or English:",
            value=st.session_state.current_query,
            placeholder="مثال: كيف أحصل على رخصة قيادة في قطر؟\nExample: How do I get a driving license in Qatar?",
            height=100
        )
        submit_button = st.form_submit_button("🔍 Search & Generate Answer", type="primary", use_container_width=True)

with col2:
    st.markdown("### 📁 Categories")
    categories = ["health", "education", "business", "transportation", 
                  "justice", "housing", "culture", "info"]
    
    category_emojis = {
        "health": "🏥",
        "education": "🎓",
        "business": "💼",
        "transportation": "🚗",
        "justice": "⚖️",
        "housing": "🏠",
        "culture": "🎭",
        "info": "ℹ️"
    }
    
    # Display categories in 2 columns
    cat_col1, cat_col2 = st.columns(2)
    
    # Split categories into two halves
    mid_point = len(categories) // 2
    categories_left = categories[:mid_point]
    categories_right = categories[mid_point:]
    
    with cat_col1:
        for cat in categories_left:
            st.markdown(f"{category_emojis.get(cat, '📄')} {cat}")
    
    with cat_col2:
        for cat in categories_right:
            st.markdown(f"{category_emojis.get(cat, '📄')} {cat}")

# Store query in session state when form is submitted to preserve it
if submit_button and query:
    st.session_state.current_query = query

# Process search when form is submitted
if submit_button and query:
    with st.spinner("🔄 Processing your query..."):
        start_time = time.time()
        try:
            # Step 1: Process query with translation
            translation_result = translator.process_query(query)
            arabic_query = translation_result['arabic_query']
            query_lang = translation_result['query_language']
            
            # Get query embedding (use Arabic query)
            query_emb = model.encode([arabic_query])[0]
            
            # Retrieve with keyword boosting
            results = retriever.search(
                query_emb,
                k=num_results,
                query_text=arabic_query  # Pass query text for keyword boosting
            )
            
            # Determine return language
            if answer_lang == "Same as query":
                return_lang = query_lang
            elif answer_lang == "Always Arabic":
                return_lang = 'ar'
            else:
                return_lang = 'en'
            
            # Generate answer
            answer_data = generator.generate_answer(
                arabic_query, results,
                language='ar',
                return_language=return_lang
            )
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Store in session state (no translation yet - do on-demand)
            st.session_state.search_results = {
                'results': results,
                'answer_data': answer_data,
                'query_lang': query_lang,
                'arabic_query': arabic_query,
                'original_query': query,  # Store original query for display
                'translation_result': translation_result,
                'avg_score': sum(r['score'] for r in results) / len(results) if results else 0,
                'display_lang': return_lang,
                'answer_lang_setting': answer_lang,
                'response_time': response_time
            }
        except Exception as e:
            st.error(f"❌ Error processing query: {str(e)}")
            st.exception(e)

# Display results if they exist in session state
if 'search_results' in st.session_state:
    # Extract from session state
    results = st.session_state.search_results['results']
    answer_data = st.session_state.search_results['answer_data']
    query_lang = st.session_state.search_results['query_lang']
    arabic_query = st.session_state.search_results['arabic_query']
    translation_result = st.session_state.search_results['translation_result']
    avg_score = st.session_state.search_results['avg_score']
    display_lang = st.session_state.search_results['display_lang']
    answer_lang_setting = st.session_state.search_results.get('answer_lang_setting', 'Same as query')
    response_time = st.session_state.search_results.get('response_time', 0)
    
    # Show translation info
    if translation_result['needs_translation']:
        st.info(f"🌐 English detected → Translated to Arabic: {arabic_query}")
    
    # Create tabs for results
    tab1, tab2, tab3 = st.tabs(["📝 Answer", "📚 Sources", "🔍 Details"])
    
    # Tab 1: Answer
    with tab1:
        # Show detected category from top result
        if results:
            top_category = results[0]['metadata']['category']
            st.info(f"📁 Top result category: **{top_category}**")
        
        st.markdown("### 💡 Answer")
        st.markdown(answer_data['answer'])
        
        # Confidence indicator
        if avg_score > 0.7:
            st.success("🎯 High confidence answer")
        elif avg_score > 0.5:
            st.info("✅ Good confidence answer")
        else:
            st.warning("⚠️ Low confidence - answer may be incomplete")
            
    # Tab 2: Sources
    with tab2:
        st.markdown("### 📚 Retrieved Sources")
        
        # Determine current desired display language based on stored setting
        if answer_lang_setting == "Same as query":
            current_display_lang = query_lang
        elif answer_lang_setting == "Always Arabic":
            current_display_lang = 'ar'
        else:  # Always English
            current_display_lang = 'en'
        
        lang_display = "English" if current_display_lang == 'en' else "Arabic"
        
        st.info(f"💡 Full documents displayed in **{lang_display}** (Setting: {answer_lang_setting})")
        
        # Initialize translation cache in session state if not exists
        if 'document_translations' not in st.session_state:
            st.session_state.document_translations = {}
        
        for i, result in enumerate(results, 1):
            score = result['score']
            source_file = result['metadata']['source_file']
            category = result['metadata']['category']
            
            # Construct full path
            full_path = f"data/{category}/{source_file}"
            
            with st.expander(
                f"**Source {i}** - {category} (Score: {score:.3f})",
                expanded=(i == 1)
            ):
                col_a, col_b = st.columns([1, 3])
                
                with col_a:
                    st.markdown("**Metadata:**")
                    st.markdown(f"📁 Category: `{category}`")
                    st.markdown(f"📄 File: `{source_file[:35]}...`")
                    st.markdown(f"📊 Score: `{score:.3f}`")
                    st.markdown(f"🌐 Language: `{lang_display}`")
                
                with col_b:
                    # Always show full document
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            full_content = f.read()
                        
                        # Create cache key for this document and language
                        cache_key = f"{full_path}_{current_display_lang}"
                        
                        # Documents are originally in Arabic
                        # Translate if current display language is English
                        if current_display_lang == 'en':
                            # Check cache first
                            if cache_key in st.session_state.document_translations:
                                full_content = st.session_state.document_translations[cache_key]
                                doc_lang = "English"
                            else:
                                # Translate and cache
                                with st.spinner(f"Translating document {i} to English..."):
                                    translated_content = translator.translate_text(full_content, 'en')
                                    st.session_state.document_translations[cache_key] = translated_content
                                    full_content = translated_content
                                    doc_lang = "English"
                        else:
                            # Keep original Arabic
                            doc_lang = "Arabic"
                        
                        st.text_area(
                            f"Full Document ({doc_lang}):",
                            full_content,
                            height=400,
                            key=f"doc_{i}_{current_display_lang}",  # Include current lang in key to force refresh
                            disabled=True
                        )
                            
                    except Exception as e:
                        st.error(f"Error loading document: {str(e)}")
            
    # Tab 3: Details
    with tab3:
        st.markdown("### 🔍 Query Analysis")
        
        col_x, col_y, col_z = st.columns(3)
        
        with col_x:
            st.markdown("**Query Info**")
            original_query = st.session_state.search_results.get('original_query', translation_result.get('original_query', arabic_query))
            st.markdown(f"- Length: {len(original_query)} chars")
            st.markdown(f"- Top Category: {results[0]['metadata']['category'] if results else 'None'}")
            st.markdown(f"- Language: {query_lang}")
        
        with col_y:
            st.markdown("**Retrieval Info**")
            st.markdown(f"- Results: {len(results)}")
            st.markdown(f"- Avg Score: {avg_score:.3f}")
            st.markdown(f"- Method: Hybrid (Semantic + Keywords)")
        
        with col_z:
            st.markdown("**Performance**")
            st.markdown(f"- Response: {response_time:.2f}s")
            st.markdown(f"- Model: MPNet")
            st.markdown(f"- LLM: Gemini 1.5")
        
        st.markdown("---")
        st.markdown("**Score Distribution:**")
        
        # Simple score visualization
        for i, result in enumerate(results, 1):
            score = result.get('rerank_score', result['score'])
            normalized = int((score / 10) * 100) if 'rerank_score' in result else int(score * 100)
            bar = "█" * (normalized // 5)
            st.markdown(f"Source {i}: {bar} {score:.3f}")

# Example queries section
st.markdown("---")
st.markdown("### 💡 Example Queries")
st.markdown("Click any example to load it into the search box:")

# Arabic examples - matched to actual documents in the database
arabic_examples = [
    ("🏥", "كيف أبحث عن طبيب في قطر؟"),
    ("💼", "كيف أعيد تفعيل رخصة تجارية؟"),
    ("🎓", "كيف أسجل في مقررات جامعة قطر؟"),
    ("🚗", "ما هي متطلبات الحصول على رخصة قيادة؟"),
    ("🏠", "كيف أحصل على بدل إيجار؟")
]

# English examples - matched to actual documents in the database
english_examples = [
    ("🏥", "How to search for a doctor in Qatar?"),
    ("💼", "How to reactivate commercial license?"),
    ("🎓", "How to register for courses at Qatar University?"),
    ("🚗", "What are the requirements for a driving license?"),
    ("🏠", "How to get rent allowance?")
]

col_ar, col_en = st.columns(2)

with col_ar:
    st.markdown("**🇶🇦 Arabic Examples:**")
    for i, (emoji, example) in enumerate(arabic_examples):
        if st.button(f"{emoji} {example[:35]}...", key=f"ex_ar_{i}", use_container_width=True):
            st.session_state.current_query = example
            st.rerun()

with col_en:
    st.markdown("**🇬🇧 English Examples:**")
    for i, (emoji, example) in enumerate(english_examples):
        if st.button(f"{emoji} {example[:35]}...", key=f"ex_en_{i}", use_container_width=True):
            st.session_state.current_query = example
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Built with ❤️ using FAISS, Multilingual Embeddings, and Google Gemini</p>
    <p><i>AraGovAssist - Qatar Government Services Assistant</i></p>
</div>
""", unsafe_allow_html=True)
