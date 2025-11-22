"""
Streamlit Demo App for Arabic Government Services RAG
"""
import streamlit as st
import sys
sys.path.append('src')

from sentence_transformers import SentenceTransformer
from category_retrieval import RerankedRetriever
from llm_generator import AnswerGenerator

# Page config
st.set_page_config(
    page_title="AraGovAssist",
    page_icon="🇶🇦",
    layout="wide"
)

# Title
st.title("🇶🇦 AraGovAssist")
st.markdown("*Arabic Government Services Intelligent Assistant*")
st.markdown("---")

# Load models (cache for performance)
@st.cache_resource
def load_models():
    """Load all models (cached)"""
    try:
        model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        
        retriever = RerankedRetriever(
            'index/embeddings.npy',
            'index/corpus_chunks.json',
            'index/corpus_meta.json'
        )
        
        generator = AnswerGenerator()
        
        return model, retriever, generator
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, None

with st.spinner("🔄 Loading models..."):
    model, retriever, generator = load_models()

if model and retriever and generator:
    st.success("✅ System ready!")
else:
    st.error("❌ Failed to load models. Check your setup.")
    st.stop()

# Settings in sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    use_category = st.checkbox("Enable category detection", value=True)
    use_reranking = st.checkbox("Enable reranking", value=True)
    use_llm = st.checkbox("Generate AI answer", value=True)
    num_results = st.slider("Number of sources", 1, 10, 3)
    
    st.markdown("---")
    st.markdown("**📊 Statistics**")
    st.metric("Documents", "34")
    st.metric("Categories", "8")
    st.metric("Retrieval Accuracy", "100%")
    
    st.markdown("---")
    st.markdown("**ℹ️ About**")
    st.markdown("Multilingual RAG system for Qatar government services using:")
    st.markdown("- Semantic search (FAISS)")
    st.markdown("- Cross-encoder reranking")
    st.markdown("- Gemini AI generation")

# Main input
query = st.text_input(
    "اسأل سؤالك هنا / Enter your question:",
    placeholder="مثال: كيف أحصل على رخصة ليموزين في قطر؟"
)

# Process query
if st.button("🔍 Search", type="primary") and query:
    with st.spinner("🔍 Searching..."):
        # Get query embedding
        query_emb = model.encode([query])[0]
        
        # Detect category
        category = None
        if use_category:
            category = retriever.detect_category(query)
            if category:
                st.info(f"📁 Detected category: **{category}**")
        
        # Retrieve
        if use_reranking:
            results = retriever.search_with_rerank(
                query, query_emb,
                category=category,
                initial_k=20,
                final_k=num_results
            )
        else:
            results = retriever.search(
                query_emb,
                category=category,
                k=num_results
            )
        
        # Generate answer if enabled
        if use_llm:
            with st.spinner("🤖 Generating answer..."):
                try:
                    answer_data = generator.generate_answer(query, results)
                    
                    # Display answer
                    st.markdown("### 📝 Answer")
                    st.markdown(answer_data['answer'])
                except Exception as e:
                    st.warning(f"Could not generate answer: {e}")
                    st.info("Showing retrieved documents instead.")
        
        # Display sources
        st.markdown("### 📚 Sources")
        for i, result in enumerate(results, 1):
            score_text = f"Score: {result['score']:.3f}"
            if 'rerank_score' in result:
                score_text += f" | Rerank: {result['rerank_score']:.3f}"
            
            with st.expander(f"Source {i}: {result['metadata']['category']} ({score_text})"):
                st.markdown(f"**File:** `{result['metadata']['source_file'].split('/')[-1]}`")
                st.markdown(f"**Search Type:** {result.get('search_type', 'N/A')}")
                st.markdown(f"**Content:**")
                st.text(result['chunk'])

# Example queries
st.markdown("---")
st.markdown("### 💡 Example Queries")

examples = [
    "كيف أحصل على رخصة ليموزين في قطر؟",
    "ما هي خطوات تسجيل المقررات في جامعة قطر؟",
    "كيف أطلب استشارة طبية عاجلة؟",
    "كيف أقدم عروض المناقصات؟",
    "ما هي إجراءات الحصول على شهادة CRA؟"
]

cols = st.columns(len(examples))
for i, example in enumerate(examples):
    with cols[i]:
        if st.button(example, key=f"ex_{i}", use_container_width=True):
            st.session_state.query = example
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Built with ❤️ using Streamlit, FAISS, and Gemini AI | "
    "<a href='https://github.com/Rayyan1704/arabic-gov-assistant-rag'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True
)
