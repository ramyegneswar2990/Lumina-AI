# Lumina AI: The Enterprise Knowledge Link 💎

[![Endee](https://img.shields.io/badge/Vector%20DB-Endee-blue.svg)](https://github.com/EndeeLabs/endee)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/Pipeline-LangChain-green.svg)](https://langchain.com)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)

## 📖 Project Overview
**Lumina AI** is an Enterprise Retrieval-Augmented Generation (RAG) system designed to enable reliable and context-aware question answering over private organizational data. It integrates **Python**, **LangChain**, and the **Endee Vector Database** to ground large language model (LLM) responses in enterprise-owned documents, APIs, and structured records.

Instead of relying on a language model’s internal knowledge, Lumina AI retrieves relevant information from trusted data sources and uses it as context for answer generation. This approach improves accuracy, transparency, and reliability when working with private or frequently updated information.

---


## 🚩 Problem Statement
Large language models are powerful but face important limitations in enterprise environments. They cannot access private or up-to-date organizational data and may generate incorrect or unsupported answers when information is missing. 

These limitations make standalone LLMs unsuitable for applications involving internal documents, APIs, or proprietary knowledge. **Lumina AI** addresses this challenge by retrieving relevant enterprise data from the **Endee Vector Database** and grounding all responses in retrieved evidence, enabling more reliable and explainable AI-driven knowledge access.

---
Live Link: https://lumina-ai231.streamlit.app/


## 🎯 Key Objectives
*   **Enable semantic search** and question answering over private enterprise data.
*   **Reduce hallucinations** by grounding responses in retrieved context.
*   **Demonstrate practical use of Endee** as a high-performance vector database.
*   **Build a realistic, production-oriented** RAG architecture.

---

## 🏗️ Technical Architecture

```text
┌─────────────────────────────────────────────────────┐
│                  USER INTERFACE                      │
│              (Streamlit - app.py)                    │
└────────────────┬────────────────────────────────────┘
                 │
        ┌────────┴─────────┐
        │  Query Processing │
        └────────┬──────────┘
                 │
    ┌────────────┴─────────────┐
    │  Embedding Generation     │
    │  (HuggingFace Embeddings) │
    └────────────┬──────────────┘
                 │
    ┌────────────┴──────────────┐
    │   Endee Vector Database    │
    │  (Docker: localhost:8080)  │
    │  - Cosine Similarity       │
    │  - 384-dim Vectors         │
    └────────────┬───────────────┘
                 │
    ┌────────────┴────────────┐
    │  Retrieval & Re-ranking │
    │  (Top-K + Confidence)   │
    └────────────┬─────────────┘
                 │
    ┌────────────┴──────────────┐
    │  Response Generation      │
    │  (Context-Grounded RAG)   │
    └───────────────────────────┘
```

---

## 🧠 System Design

### 1️⃣ Multi-Source Data Ingestion
Lumina AI supports ingestion from:
*   **PDF documents**: Policies, manuals, and reports.
*   **Web URLs**: With automatic noise and boilerplate removal.
*   **CSV / Database records**: Structured tabular data.
*   **REST API / JSON responses**: Dynamic data from internal services.

### 2️⃣ Semantic Text Processing
*   Text is split into **1000-character chunks** with **200-character overlap**.
*   Metadata is attached to each chunk (source, type, origin) for full traceability.

### 3️⃣ Vector Storage with Endee
*   Embeddings are generated using `all-MiniLM-L6-v2` (384-dimensional).
*   Vectors and metadata are stored in **Endee**.
*   **Cosine similarity** is used for high-precision semantic retrieval.

### 4️⃣ Retrieval-Augmented Generation (RAG)
*   User queries are embedded and matched against stored vectors.
*   **Top-K (K=15)** relevant chunks are retrieved and filtered to skip noise.
*   Retrieved context is passed to the language model for grounded response generation.

### 5️⃣ Interactive User Interface
*   Modern **Streamlit-based** chat interface.
*   Displays retrieved sources and **similarity-based confidence scores**.
*   Built-in tools for clearing and re-indexing data.

---
## 🔗 DashBoarad & output:
<img width="1831" height="761" alt="image" src="https://github.com/user-attachments/assets/d20f7c76-7464-4963-9981-782111c844a9" />
<img width="1345" height="578" alt="image" src="https://github.com/user-attachments/assets/f30815e1-5928-4738-b277-0444b06f5a5c" />

:

## 🔗 Role of Endee Vector Database
Endee serves as the **core semantic memory layer** of Lumina AI. It is utilized for:
*   Storing high-dimensional embeddings.
*   Performing similarity-based semantic search.
*   Managing vector lifecycle (index creation, clearing, re-indexing).

> **Note:** Endee replaces traditional vector stores such as FAISS or Milvus and is the **only** vector database used in this project.

---

## 🛠️ Key Features
*   🔍 **Semantic Search**: Understands meaning, not just keywords.
*   📄 **Multi-Source Ingestion**: PDF, Web, CSV, and API support.
*   🧠 **Grounded Responses**: AI answers only based on your data.
*   📊 **Confidence Scoring**: See exactly how relevant the data is.
*   🧹 **One-Click Reset**: Easy cleanup of the vector index.
*   💬 **Interactive UI**: Sleek, professional Streamlit interface.

---

## 📂 Project Structure
```text
Endee_Assignment/
├── app.py                 # Streamlit application (UI & Logic)
├── src/
│   ├── __init__.py
│   ├── vector_store.py    # Endee client wrapper & fallback
│   └── ingestion.py       # Data loaders and processors
├── data/
│   └── customers.csv      # Sample structured data
├── docker-compose.yml     # Endee server configuration
├── requirements.txt       # Project dependencies
└── README.md              # Documentation
```

---

## 🚀 Getting Started

### Prerequisites
*   **Python 3.10+**
*   **Docker Desktop** (Required for Endee Server)

### Setup & Run
1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Start Endee server**:
    ```bash
    docker-compose up -d
    ```
3.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

Open your browser at: 👉 [http://localhost:8501](http://localhost:8501)

---

## ✅ Assignment Compliance
*   ✔ **Retrieval-Augmented Generation (RAG)** pipeline implementation.
*   ✔ **Endee** used as the only vector database.
*   ✔ **Multi-source** data ingestion support.
*   ✔ **Semantic retrieval** with confidence scoring.
*   ✔ **LangChain-based** document processing.
*   ✔ **Interactive user interface** with Streamlit.
*   ✔ **Professional documentation** and modular code.

---

## 🔮 Future Enhancements
*   **Advanced LLM support**: Native integration for local models like Llama 3.
*   **Metadata filtering**: Filter search results by date or source type.
*   **Authentication**: Secure user login and access control.
*   **Batch Monitoring**: Dashboard for tracking ingestion speeds and query latency.

---

## 🎓 Academic & Learning Outcomes
This project demonstrates:
*   Practical integration of **vector databases** in AI workflows.
*   **Enterprise-ready** RAG architecture design.
*   Integration of LLMs with **private, unstructured data**.
*   Clean, modular, and **explainable system design**.

---

## 📜 License & Credits
*   **Endee Vector Database** — [Endee Labs](https://github.com/EndeeLabs/endee)
*   **LangChain** — Document processing framework
*   **Sentence Transformers** — Embedding models
*   **Streamlit** — Web application framework
