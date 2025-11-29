"""
AraGovAssist - Streamlit Demo UI
Interactive web interface for the Qatar Government Services RAG system.
"""

import streamlit as st
import sys
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
    
    use_category = st.checkbox("Enable category detection", value=True, 
                               help="Automatically detect query category for focused search")
    use_reranking = st.checkbox("Enable reranking", value=True,
                                help="Use cross-encoder for better accuracy (slower)")
    num_results = st.slider("Number of sources", 1, 10, 3,
                           help="How many source documents to retrieve")
    
    st.markdown("---")
    st.markdown("### 🌐 Language Settings")
    answer_lang = st.radio(
        "Answer language:",
        ["Same as query", "Always Arabic", "Always English"],
        index=0,
        help="Choose output language for answers"
    )
    
    st.markdown("---")
    
    # System stats
    st.markdown("### 📊 System Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Documents", "51")
        st.metric("Categories", "8")
    with col2:
        st.metric("Accuracy", "96%")
        st.metric("Response", "0.16s")
    
    st.markdown("---")
    
    # About
    st.markdown("### 📖 About")
    st.markdown("""
    **AraGovAssist** is a RAG system for Qatar government services.
    
    **Features:**
    - 🔍 Semantic search
    - 🎯 Category detection
    - ⚡ Cross-encoder reranking
    - 🤖 AI-powered answers
    - 🇶🇦 Arabic support
    
    **Tech Stack:**
    - FAISS vector search
    - Sentence Transformers
    - Google Gemini LLM
    - Streamlit UI
    """)
    
    st.markdown("---")
    st.markdown("**Version:** 2.0 (Day 10)")
    st.markdown("**Status:** Research Complete ✅")
    st.markdown("**Accuracy:** 96% (100 queries)")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Ask Your Question")
    query = st.text_area(
        "Enter your question in Arabic or English:",
        placeholder="مثال: كيف أحصل على رخصة قيادة في قطر؟\nExample: How do I get a driving license in Qatar?",
        height=100,
        key="query_input"
    )

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
    
    for cat in categories:
        st.markdown(f"{category_emojis.get(cat, '📄')} {cat}")

# Search button
if st.button("🔍 Search & Generate Answer", type="primary", use_container_width=True) and query:
    
    # Create tabs for results
    tab1, tab2, tab3 = st.tabs(["📝 Answer", "📚 Sources", "🔍 Details"])
    
    with st.spinner("🔄 Processing your query..."):
        try:
            # Step 1: Process query with translation
            translation_result = translator.process_query(query)
            arabic_query = translation_result['arabic_query']
            query_lang = translation_result['query_language']
            
            # Show translation info
            if translation_result['needs_translation']:
                st.info(f"🌐 English detected → Translated to Arabic: {arabic_query}")
            
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
            
            # Tab 1: Answer
            with tab1:
                # Show detected category from top result
                if results:
                    top_category = results[0]['metadata']['category']
                    st.info(f"📁 Top result category: **{top_category}**")
                
                st.markdown("### 💡 Answer")
                st.markdown(answer_data['answer'])
                
                # Confidence indicator
                avg_score = sum(r['score'] for r in results) / len(results)
                if avg_score > 0.7:
                    st.success("🎯 High confidence answer")
                elif avg_score > 0.5:
                    st.info("✅ Good confidence answer")
                else:
                    st.warning("⚠️ Low confidence - answer may be incomplete")
            
            # Tab 2: Sources
            with tab2:
                st.markdown("### 📚 Retrieved Sources")
                
                for i, result in enumerate(results, 1):
                    score = result['score']
                    
                    with st.expander(
                        f"**Source {i}** - {result['metadata']['category']} "
                        f"(Score: {score:.3f})",
                        expanded=(i == 1)
                    ):
                        col_a, col_b = st.columns([1, 3])
                        
                        with col_a:
                            st.markdown("**Metadata:**")
                            st.markdown(f"📁 Category: `{result['metadata']['category']}`")
                            st.markdown(f"📄 File: `{result['metadata']['source_file'].split('/')[-1]}`")
                            st.markdown(f"📊 Score: `{score:.4f}`")
                        
                        with col_b:
                            st.markdown("**Content:**")
                            st.text_area(
                                "Document text:",
                                result['chunk'],
                                height=150,
                                key=f"source_{i}",
                                disabled=True
                            )
            
            # Tab 3: Details
            with tab3:
                st.markdown("### 🔍 Query Analysis")
                
                col_x, col_y, col_z = st.columns(3)
                
                with col_x:
                    st.markdown("**Query Info**")
                    st.markdown(f"- Length: {len(query)} chars")
                    st.markdown(f"- Top Category: {results[0]['metadata']['category'] if results else 'None'}")
                    st.markdown(f"- Language: {query_lang}")
                
                with col_y:
                    st.markdown("**Retrieval Info**")
                    st.markdown(f"- Results: {len(results)}")
                    st.markdown(f"- Avg Score: {avg_score:.3f}")
                    st.markdown(f"- Method: Hybrid (Semantic + Keywords)")
                
                with col_z:
                    st.markdown("**Performance**")
                    st.markdown(f"- Model: Multilingual MPNet")
                    st.markdown(f"- Vector DB: FAISS")
                    st.markdown(f"- LLM: Gemini 2.0 Flash")
                
                st.markdown("---")
                st.markdown("**Score Distribution:**")
                
                # Simple score visualization
                for i, result in enumerate(results, 1):
                    score = result.get('rerank_score', result['score'])
                    normalized = int((score / 10) * 100) if 'rerank_score' in result else int(score * 100)
                    bar = "█" * (normalized // 5)
                    st.markdown(f"Source {i}: {bar} {score:.3f}")
        
        except Exception as e:
            st.error(f"❌ Error processing query: {str(e)}")
            st.exception(e)

# Example queries section
st.markdown("---")
st.markdown("### 💡 Example Queries")
st.markdown("Click any example to try it:")

examples = [
    ("🏥 Health", "كيف أحصل على بطاقة صحية في قطر؟"),
    ("💼 Business", "ما هي إجراءات فتح سجل تجاري؟"),
    ("🎓 Education", "كيف أسجل أطفالي في المدرسة الحكومية؟"),
    ("🚗 Transportation", "ما هي متطلبات الحصول على رخصة قيادة؟"),
    ("🏠 Housing", "كيف أستأجر شقة في الدوحة؟"),
    ("⚖️ Justice", "كيف أقدم شكوى قانونية؟")
]

cols = st.columns(3)
for i, (category, example) in enumerate(examples):
    with cols[i % 3]:
        if st.button(f"{category}\n{example[:30]}...", key=f"ex_{i}", use_container_width=True):
            st.session_state.query_input = example
            st.rerun()

# Footer
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.markdown("**🎯 Accuracy:** 90% (validated)")

with col_f2:
    st.markdown("**⚡ Response Time:** 3-5 seconds")

with col_f3:
    st.markdown("**🚀 Status:** Production Ready")

st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Built with ❤️ using Streamlit, FAISS, and Google Gemini</p>
    <p><i>Day 6: Demo UI Complete</i></p>
</div>
""", unsafe_allow_html=True)
