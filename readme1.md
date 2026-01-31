Project Overview

Lumina AI is an Enterprise Retrieval-Augmented Generation (RAG) system designed to enable reliable and context-aware question answering over private organizational data.
It integrates Python, LangChain, and the Endee Vector Database to ground large language model (LLM) responses in enterprise-owned documents, APIs, and structured records.

Instead of relying on a language model’s internal knowledge, Lumina AI retrieves relevant information from trusted data sources and uses it as context for answer generation. This approach improves accuracy, transparency, and reliability when working with private or frequently updated information.

🚩 Problem Statement

Large language models are powerful but face important limitations in enterprise environments. They cannot access private or up-to-date organizational data and may generate incorrect or unsupported answers when information is missing.

These limitations make standalone LLMs unsuitable for applications involving internal documents, APIs, or proprietary knowledge.

Lumina AI addresses this challenge by retrieving relevant enterprise data from the Endee Vector Database and grounding all responses in retrieved evidence, enabling more reliable and explainable AI-driven knowledge access.

🎯 Key Objectives

Enable semantic search and question answering over private enterprise data

Reduce hallucinations by grounding responses in retrieved context

Demonstrate practical use of Endee as a vector database

Build a realistic, production-oriented RAG architecture

🏗️ Technical Architecture & Workflow
Data Sources (PDF | Web | CSV | API)
            ↓
     Text Extraction & Cleaning
            ↓
   Chunking & Embedding Generation
            ↓
      Endee Vector Database
            ↓
   Semantic Retrieval & Re-ranking
            ↓
   Context-Grounded LLM Response
            ↓
        Streamlit UI
🧠 System Design
1️⃣ Multi-Source Data Ingestion

Lumina AI supports ingestion from:

PDF documents (policies, manuals, reports)

Web URLs (with noise and boilerplate removal)

CSV / database-like records

REST API / JSON responses

2️⃣ Semantic Text Processing

Text is split into 1000-character chunks with 200-character overlap

Metadata is attached to each chunk (source, type, origin)

3️⃣ Vector Storage with Endee

Embeddings are generated using all-MiniLM-L6-v2 (384-dimensional)

Vectors and metadata are stored in Endee

Cosine similarity is used for semantic retrieval

4️⃣ Retrieval-Augmented Generation (RAG)

User queries are embedded and matched against stored vectors

Top-K relevant chunks are retrieved and re-ranked

Retrieved context is passed to the language model for grounded response generation

5️⃣ Interactive User Interface

Streamlit-based chat interface

Displays retrieved sources and similarity scores

Allows clearing and re-indexing data

🔗 Role of Endee Vector Database

Endee serves as the core semantic memory layer of Lumina AI.

It is used for:

Storing high-dimensional embeddings

Performing similarity-based semantic search

Managing vector lifecycle (index creation, clearing, re-indexing)

Endee replaces traditional vector stores such as FAISS or Milvus and is the only vector database used in this project.

🛠️ Key Features

🔍 Semantic search over enterprise data

📄 Multi-source ingestion (PDF, Web, CSV, API)

🧠 Context-grounded RAG responses

📊 Similarity-based confidence scoring

🧹 One-click vector index reset

💬 Interactive Streamlit chat UI

📂 Project Structure
Endee_Assignment/
├── app.py                 # Streamlit application
├── src/
│   ├── __init__.py
│   ├── vector_store.py    # Endee client wrapper
│   └── ingestion.py       # Data loaders and processors
├── data/
│   └── customers.csv      # Sample structured data
├── docker-compose.yml     # Endee server setup
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
🚀 Getting Started
Prerequisites

Python 3.10+

Docker Desktop

Setup & Run
# Install dependencies
pip install -r requirements.txt


# Start Endee server
docker-compose up -d


# Run the application
streamlit run app.py

Open your browser at:
👉 http://localhost:8501

✅ Assignment Compliance

✔ Retrieval-Augmented Generation (RAG) pipeline

✔ Endee used as the only vector database

✔ Multi-source data ingestion

✔ Semantic retrieval with confidence scoring

✔ LangChain-based document processing

✔ Interactive user interface

✔ Clear documentation and modular code

🔮 Future Enhancements

LLM API integration for richer responses

Metadata-based filtering

Authentication and access control

Batch ingestion and monitoring tools

🎓 Academic & Learning Outcomes

This project demonstrates:

Practical use of vector databases

Enterprise-ready RAG architecture

Integration of LLM workflows with private data

Clean, modular, and explainable system design

📜 License & Credits

Endee Vector Database — Endee Labs

LangChain — Document processing framework

Sentence Transformers — Embedding models