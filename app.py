import streamlit as st
import os
import time
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Import our modules
from src.vector_store import EndeeService
from src.ingestion import IngestionPipeline

# Page Config
st.set_page_config(
    page_title="Lumina AI | Enterprise Knowledge Link",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Wow" factor
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(45deg, #FF4B2B, #FF416C); 
        color: white;
        border: none;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4);
    }
    .stTextInput>div>div>input {
        background-color: #262730;
        color: white;
        border-radius: 8px;
    }
    .css-1y4p8pa {
        padding-top: 2rem;
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    .metric-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #374151;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialization
@st.cache_resource
def get_resources():
    st.write("Initializing Models and Database...")
    embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = EndeeService(collection_name="enterprise_knowledge", dimension=384)
    pipeline = IngestionPipeline()
    return embed_model, vector_store, pipeline

if 'is_initialized' not in st.session_state:
    st.session_state['embed_model'], st.session_state['vector_store'], st.session_state['pipeline'] = get_resources()
    st.session_state['chat_history'] = []
    st.session_state['is_initialized'] = True

# Sidebar
with st.sidebar:
    st.title("Data Ingestion")
    st.markdown("Add knowledge to the **Endee Link** database.")
    
    upload_type = st.selectbox("Source Type", ["Web URL", "PDF Document", "Customers Database", "REST API / JSON"])
    
    if upload_type == "Web URL":
        url_input = st.text_area("Enter URLs (one per line)", placeholder="https://example.com/page1\nhttps://example.com/page2")
        if st.button("Ingest URLs"):
            urls = [u.strip() for u in url_input.split('\n') if u.strip()]
            if urls:
                with st.spinner(f"Scraping {len(urls)} URLs..."):
                    docs = st.session_state['pipeline'].load_web(urls)
                    if docs:
                        embeddings = st.session_state['embed_model'].embed_documents([d.page_content for d in docs])
                        st.session_state['vector_store'].add_documents(docs, embeddings)
                        st.success(f"Successfully ingested {len(docs)} chunks from {len(urls)} URLs.")
    
    elif upload_type == "PDF Document":
        uploaded_files = st.file_uploader("Upload PDF(s)", type=['pdf'], accept_multiple_files=True)
        if uploaded_files and st.button("Process PDF(s)"):
            all_docs = []
            with st.spinner(f"Parsing {len(uploaded_files)} PDF(s)..."):
                for uploaded_file in uploaded_files:
                    # Save temp with unique name per file
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    docs = st.session_state['pipeline'].load_pdf(temp_path)
                    all_docs.extend(docs)
                    # Cleanup
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                
                if all_docs:
                    embeddings = st.session_state['embed_model'].embed_documents([d.page_content for d in all_docs])
                    st.session_state['vector_store'].add_documents(all_docs, embeddings)
                    st.success(f"Successfully ingested {len(all_docs)} chunks from {len(uploaded_files)} files.")

    elif upload_type == "Customers Database":
        st.info("Simulating connection to SQL/CSV database (Data Source: data/customers.csv)")
        if st.button("Sync Database"):
            with st.spinner("Syncing records..."):
                path = os.path.abspath("data/customers.csv")
                docs = st.session_state['pipeline'].load_csv(path)
                if docs:
                    embeddings = st.session_state['embed_model'].embed_documents([d.page_content for d in docs])
                    st.session_state['vector_store'].add_documents(docs, embeddings)
                    st.success(f"Synced {len(docs)} customer records.")

    elif upload_type == "REST API / JSON":
        json_input = st.text_area("Paste JSON / API Response", height=150, placeholder='{"key": "value"}')
        if st.button("Process JSON"):
            import json
            try:
                data = json.loads(json_input)
                docs = st.session_state['pipeline'].load_json(data)
                if docs:
                    embeddings = st.session_state['embed_model'].embed_documents([d.page_content for d in docs])
                    st.session_state['vector_store'].add_documents(docs, embeddings)
                    st.success(f"Ingested data from JSON response.")
            except Exception as e:
                st.error(f"Invalid JSON: {e}")

    st.markdown("---")
    st.markdown("### 🔑 Advanced Configuration")
    oa_key = st.text_input("OpenAI API Key (Optional)", type="password", key="openai_key_input")
    if oa_key:
        st.session_state['openai_api_key'] = oa_key

    if st.button("🗑️ Clear All Knowledge Data"):
        st.session_state['vector_store'].clear_data()
        st.success("Knowledge base cleared! You can now re-ingest fresh data.")
        st.rerun()

    st.markdown("---")
    st.markdown("### System Status")
    connected = st.session_state['vector_store'].connected
    st.markdown(f"**Endee DB Connection:** {'🟢 Online' if connected else '🔴 Offline (Mock Mode)'}")
    st.markdown(f"**Knowledge Items:** {len(st.session_state['vector_store'].mock_store)}")

# Main Chat Interface
st.title("Lumina AI")
st.markdown("### The Enterprise Knowledge Link")
st.markdown("Ask questions grounded in your private documents. Powered by an advanced **Vector Search Engine**.")

# Chat container
for msg in st.session_state['chat_history']:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
             with st.expander("🔍 Inspection: Source Data and Evidence"):
                 for s in msg["sources"]:
                     st.write(f"**Relevance Track:** {s.get('score', 0):.4f}")
                     st.caption(f"Source: {s.get('metadata', {}).get('source', 'Unknown')}")
                     st.info(s.get('text'))

query = st.chat_input("Ask a question about your documents...")

if query:
    # User message
    st.session_state['chat_history'].append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # RAG Retrieval
    with st.spinner("Searching Endee Vector DB..."):
        query_vec = st.session_state['embed_model'].embed_query(query)
        # Deep search (k=15) to ensure we find technical content beyond T.O.C.
        results = st.session_state['vector_store'].search(query_vec, k=15)

    # Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Synthesizing answer..."):
            # Filtering: Keep chunks that carry high semantic signal (longer, non-empty, unique)
            # We want to skip Table of Contents fragments
            best_chunks = []
            seen_text = set()
            for r in results:
                txt = r['text'].strip()
                # Skip common T.O.C. indicators
                if any(x in txt.lower() for x in ["contents", "references", "further reading", "navigation"]):
                    continue
                if len(txt) > 80 and txt not in seen_text:
                    best_chunks.append(r)
                    seen_text.add(txt)
            
            # If filtering too strict, fall back to top 5 matches
            if len(best_chunks) < 2:
                best_chunks = results[:5]
            
            # Construct Rich Context
            context_text = "\n\n".join([f"DATA CHUNK {i+1}:\n{r['text']}" for i, r in enumerate(best_chunks)])
            
            # Check for OpenAI Key (Strictly clean the input)
            api_key = str(st.session_state.get('openai_api_key', '')).strip()
            
            if api_key and (api_key.startswith('sk-') or len(api_key) > 40):
                try:
                    from openai import OpenAI
                    client = OpenAI(api_key=api_key)
                    # Using gpt-4o-mini for state-of-the-art cost-effective RAG
                    completion = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a senior technical expert. Answer the question specifically using the provided Data Chunks. Be highly detailed and avoid mentioning 'Match numbers'. If the information is missing, explain exactly what part of the user query wasn't covered in the source text."},
                            {"role": "user", "content": f"DATA CHUNKS:\n{context_text}\n\nUSER QUESTION: {query}"}
                        ]
                    )
                    response = completion.choices[0].message.content
                except Exception as e:
                    response = f"⚠️ Generation error: {str(e)}\n\n*Falling back to local data view...*\n\n"
                    # Append local view as fallback
                    for i, r in enumerate(best_chunks[:3]):
                        response += f"**[{i+1}]** {r['text'][:500]}...\n\n"
            else:
                # Local Knowledge Synthesis
                response = f"### 📊 Direct Evidence Analysis from Vector Store\n\n"
                response += "*(Note: No valid OpenAI key detected. Showing direct matches from Endee database.)*\n\n"
                for i, r in enumerate(best_chunks[:4]):
                    response += f"**Information Block {i+1}:**\n{r['text'][:800]}\n\n"
                
                response += "\n---\n*Synthesis produced from top semantic matches. If the results look like citations, click 'Clear All Knowledge Data' and re-ingest the URL to use the new filtered engine.*"

        st.markdown(response)
        st.session_state['chat_history'].append({"role": "assistant", "content": response, "sources": best_chunks})
        
        if best_chunks:
            with st.expander("🔍 Deep Dive: Verifying Retrieval Accuracy"):
                 for i, s in enumerate(best_chunks):
                     st.write(f"**Chunk ID:** {i+1} | **Score:** {s.get('score', 0):.4f}")
                     st.caption(f"Source: {s.get('metadata',{}).get('source')}")
                     st.info(s.get('text'))
