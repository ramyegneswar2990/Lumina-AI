# Lumina AI: The Enterprise Knowledge Link

## �️ Project Overview & Problem Statement
In the modern enterprise, Large Language Models (LLMs) often suffer from **hallucinations** and a lack of access to real-time, private documents. **Lumina AI** is an Advanced Multi-Source RAG (Retrieval-Augmented Generation) system designed to solve this. By grounding AI responses in verified corporate data, Lumina AI ensures every answer is factually accurate, verifiable, and private.

## 🏗️ System Design & Technical Approach
Lumina AI follows a modular RAG architecture:
1.  **Multi-Source Ingestion**:
    *   **Web URLs**: Advanced noise filtering (removes citations, ads, and navigation boilerplate from sites like Wikipedia).
    *   **PDFs**: Deep parsing of complex documents.
    *   **Structured Data**: Direct syncing from CSV databases.
    *   **REST API / JSON**: Real-time processing of API responses.
2.  **Processing**: Automatic text chunking using `RecursiveCharacterTextSplitter` (1000 chars) with 200-char context overlap.
3.  **Embeddings**: Generation of 384-dimensional semantic vectors using `all-MiniLM-L6-v2`.
4.  **Retrieval**: Deep semantic search (K=15) with context-aware filtering to prioritize informative paragraphs over chapter titles or TOC headers.
5.  **Synthesis**: Intelligent answer generation using either Local Evidence Synthesis or GPT-4o-mini.

## ⚡ The Power of Endee (Vector Database)
The core of Lumina AI is the **Endee Vector Database**. We chose Endee for its high-performance semantic retrieval and seamless Docker-based deployment.

*   **Deployment**: Runs as a localized containerized service via Docker for maximum security and performance.
*   **Integration**: Uses the Endee Python SDK for sub-millisecond similarity search across enterprise knowledge.
*   **Accuracy**: Utilizes `cosine` similarity to ensure the highest mathematical match between user queries and document meanings.
*   **Robustness**: Features a fail-safe connection mechanism that ensures Lumina AI remains functional even if the vector server is temporarily unavailable.

## � Setup & Execution Instructions

### Prerequisites
- Python 3.10+
- Docker Desktop
- OpenAI API Key (Optional, for smart synthesis)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Vector Engine (Endee)
```bash
docker-compose up -d
```

### 3. Launch Lumina AI
```bash
streamlit run app.py
```

### 4. Direct Access
Open your browser and navigate to `http://localhost:8501`.

---
*Developed as a production-ready demonstration of Enterprise RAG architecture leveraging the Endee Vector Engine.*
