# Lumina AI: Enterprise Knowledge Link 💎

[![Endee](https://img.shields.io/badge/Vector%20DB-Endee-blue.svg)](https://github.com/EndeeLabs/endee)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/Pipeline-LangChain-green.svg)](https://langchain.com)

**Lumina AI** is a state-of-the-art **Retrieval-Augmented Generation (RAG)** platform designed to bridge the gap between static enterprise data and dynamic AI intelligence. It allows organizations to ground LLM responses in their own private, real-time data using the **Endee Vector Database**.

---

## 🚩 The Problem Statement
Standard AI models (like GPT-4) suffer from two major flaws in an enterprise setting:
1. **Knowledge Cutoffs**: They don't know about events that happened yesterday.
2. **Hallucination**: They confidently make up facts when they don't have access to your private company documents, PDFs, or internal APIs.

**Lumina AI** solves this by implementing a "Trusted Knowledge Layer." Instead of relying on the AI's memory, it searches your specific documents first and uses that evidence to generate 100% factual answers.

---

## 🏗️ Technical Approach & System Design

Lumina AI uses a modern, modular architecture:

1. **Smart Ingestion Layer**: 
   - **PDF/CSV**: High-fidelity parsing of business documents.
   - **Web Scrubbing**: A custom engine that strips out boilerplate (ads, navbars, citations) to ensure only "clean" knowledge is indexed.
   - **REST/JSON**: Direct integration for live API responses.
2. **Semantic Text Processing**: Documents are broken into 1000-character chunks with a 200-character context overlap, ensuring no technical detail is lost.
3. **Vector Core**: High-dimensional embeddings are generated and stored in **Endee**.
4. **Contextual Retrieval**: A deep-search algorithm (K=15) retrieves the most mathematically relevant paragraphs.
5. **Intelligent Synthesis**: A dual-brain system that uses **GPT-4o-mini** for summaries, with a robust Local Synthesis fallback.

---

## 🔗 How Endee is Utilized
Endee is the heart of Lumina AI. We leverage its high-performance vector search to handle sub-millisecond similarity queries.

*   **Custom Indexing**: We initialize an Endee collection with `space_type="cosine"`, optimized for semantic similarity.
*   **Mathematical Precision**: Every answer is backed by a **Similarity Score** (0.0 to 1.0) calculated directly by the Endee engine.
*   **Lifecycle Management**: We implemented a **Deep Clear** protocol that allows one-click deletion and re-initialization of the Endee index for fresh data cycles.

---

## 🚀 Getting Started

### 1. Prerequisites
*   **Python 3.10+**
*   **Docker Desktop** (to run the Endee Server)

### 2. Infrastructure Setup
Run the Endee Vector Server using Docker:
```bash
docker-compose up -d
```

### 3. Application Installation
```bash
# Clone the repository
git clone https://github.com/ramyegneswar2990/Lumina-AI.git
cd Lumina-AI

# Install dependencies
pip install -r requirements.txt
```

### 4. Run Lumina AI
```bash
streamlit run app.py
```

---

## 🛠️ Feature Deep Dive
*   💎 **Lumina UI**: A premium dark-mode interface designed for power users.
*   🧹 **Noise Filtering**: Automatically skips Wikipedia references and chapter titles to find the "meat" of the text.
*   🔄 **Live Status**: Real-time heartbeat monitor for the Endee connection.
*   📊 **Evidence Box**: Expand any answer to see the exact paragraph on which the AI based its response.

---

## 📂 Project Structure
*   `app.py`: The UI and RAG orchestration engine.
*   `src/vector_store.py`: The Endee client wrapper and fallback logic.
*   `src/ingestion.py`: Advanced data loading and noise-filtering logic.
*   `docker-compose.yml`: Infrastructure-as-code for the Endee Vector Server.

---

Developed with ❤️ using **Endee Link Vector Database** for Enterprise Intelligence.
