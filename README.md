# Lumina AI 💎
### The Enterprise Knowledge Link

Lumina AI is an advanced **Retrieval-Augmented Generation (RAG)** platform designed to bridge the gap between massive enterprise data silos and actionable intelligence. By utilizing the **Endee Vector Database**, Lumina AI provides factually grounded, verifiable answers to complex queries across multiple data formats.

---

## 📖 Project Overview & Problem Statement

### The Problem
Traditional enterprise search relies on keywords, often failing to understand the *intent* behind a query. Meanwhile, standard AI models (like GPT-4) suffer from **hallucinations** and lack access to real-time, private, or domain-specific data.

### The Solution: Lumina AI
Lumina AI implements a "Librarian" approach (RAG). Instead of guessing an answer, it:
1.  **Ingests** data from PDFs, Web URLs, CSVs, and REST APIs.
2.  **Indexes** that data into a high-performance Vector Database (**Endee**).
3.  **Retrieves** the most relevant facts based on semantic meaning.
4.  **Synthesizes** a response that is 100% grounded in the source material.

---

## 🛠️ System Design & Technical Approach

Lumina AI is built with a modular architecture to ensure scalability and reliability:

-   **Data Ingestion Layer**: Custom pipeline using `LangChain` loaders. Features advanced HTML cleaning to strip web noise (ads/navbars) from Wikipedia and other sites.
-   **Embedding Engine**: Uses `sentence-transformers/all-MiniLM-L6-v2` to transform text into 384-dimensional dense vectors.
-   **Vector Storage (The Heart)**: **Endee Vector Database** running in Docker for sub-millisecond similarity search.
-   **Orchestration**: A robust Python backend that handles multi-source logic and semantic filtering.
-   **User Interface**: A premium Streamlit dashboard with dark mode, real-time status monitoring, and source transparency.

---

## 🚀 How Endee is Used

Endee serves as the centralized memory for Lumina AI. We leverage its high-performance vector operations for:

1.  **Index Management**: Dynamic creation and deletion of vector collections.
2.  **Vector Search**: Using **Cosine Similarity** to find the mathematical "distance" between a user's question and the stored knowledge chunks.
3.  **Memory Reset**: Implementing the `client.delete_index` capability to allow users to wipe and refresh their knowledge base instantly.

```python
# Initialization example
from endee import Endee
client = Endee(token="admin_secret")

# High-speed search
results = index.search(query_vector=query_vec, limit=15)
```

---

## 💻 Setup & Execution Instructions

### 1. Prerequisites
-   Python 3.10+
-   Docker Desktop (for the Endee Server)

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/ramyegneswar2990/Lumina-AI.git
cd Lumina-AI

# Install dependencies
pip install -r requirements.txt
```

### 3. Start the Vector Server
```bash
# Launch Endee via Docker
docker-compose up -d
```

### 4. Launch Lumina AI
```bash
streamlit run app.py
```

### 5. Access the Interface
Open your browser and navigate to: `http://localhost:8501`

---

## ✅ Key Features
-   **Multi-Source**: Ingest PDF, Web, CSV, and JSON/API data.
-   **Noise Filtering**: Automatic removal of website headers/footers for cleaner answers.
-   **Confidence Scoring**: Every answer includes a mathematical similarity score.
-   **LLM Choice**: Works offline with local synthesis or connects to GPT-4o-mini for expert summaries.
-   **Knowledge Control**: One-click "Clear All Knowledge" button to reset the database.

---
*Built for the Endee RAG Assignment.*
