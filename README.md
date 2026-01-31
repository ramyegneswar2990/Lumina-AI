# Endee Enterprise RAG System

A high-performance Retrieval Augmented Generation (RAG) system using **Endee** as the core vector database. This project demonstrates how to build an enterprise-grade search and chat application with Python, LangChain, and Streamlit.

## 🚀 Features

- **Endee Vector Database**: High-performance vector storage and retrieval replacing FAISS/Milvus.
- **Multi-Source Ingestion**: Support for PDF documents, Web URLs, and CSV/Database records.
- **Semantic Search**: Uses `all-MiniLM-L6-v2` embeddings for accurate semantic matching.
- **Advanced RAG Pipeline**:
    - Chunking with `RecursiveCharacterTextSplitter`
    - Embedding generation
    - Vector storage in Endee
    - Similarity search with confidence scores
- **Interactive UI**: Modern Streamlit interface with "Dark Mode" aesthetics.

## 🛠️ Architecture

1.  **Ingestion Layer**: `src/ingestion.py` handles loading and chunking of data from various sources.
2.  **Storage Layer**: `src/vector_store.py` manages the connection to **Endee Server** (see Docker setup) and handles vector insertion/querying. It includes a robust *Offline Mock Mode* for demonstration without the server.
3.  **Application Layer**: `app.py` provides the chat interface and orchestrates the RAG flow.

## 📦 Tech Stack

- **Python 3.10+**
- **Vector DB**: [Endee](https://github.com/EndeeLabs/endee)
- **Framework**: LangChain, Streamlit
- **Embeddings**: SentenceTransformers (HuggingFace)

## 🏎️ Quick Start

### 1. Prerequisites
- Python installed
- Docker installed (for running Endee Server)

### 2. Setup Environment

```bash
# Create virtual environment
python -m venv venv
# Activate it (Windows)
.\venv\Scripts\activate
# Activate it (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start Endee Vector Database
To use the full power of Endee, run the server using Docker:

```bash
docker-compose up -d
```
*Note: If you cannot run Docker, the application will automatically fall back to an in-memory simulation mode so you can still test the UI and logic.*

### 4. Run the Application

```bash
streamlit run app.py
```

**Note**: If you see "🔴 Offline (Mock Mode)" in the sidebar even though Docker is running, simply refresh the browser page. The Endee server may take a few seconds to fully initialize.

## 📘 Usage Guide

1.  Open the Streamlit app in your browser (usually `http://localhost:8501`).
2.  **Ingest Data**: Use the sidebar to upload a PDF, enter a Website URL, or sync the mock "Customers Database".
3.  **Ask Questions**: Type your query in the chat box. The system will retrieve relevant context from Endee and generate a response.
4.  **Inspect Sources**: Expand the "View Retrieval Sources" to see exactly what data was fetched and the similarity confidence scores.

## 📝 Assignment Detail
This project satisfies the requirement to replace FAISS/Milvus with **Endee**, utilizing its Python SDK (`endee` package) to interface with the core database engine.
