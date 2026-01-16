Website Question Answering Chatbot (RAG-Based)

# Project Overview

This project implements a Retrieval-Augmented Generation (RAG) based chatbot that allows users to ask natural language questions about a given website.
The system scrapes website content, indexes it into a vector database, and generates answers strictly grounded in the website’s content, preventing hallucinations or external knowledge usage.

# A Streamlit-based user interface enables users to:

    Enter a website URL

    Index the website

    Ask questions in a conversational chat interface

    Receive context-aware answers limited to the indexed website

# Architecture Explanation

The system follows a modular RAG architecture:

    User (Streamlit UI)
    ↓
    Website URL Input
    ↓
    Web Scraper
    ↓
    Semantic Chunking (spaCy sentence-based)
    ↓
    Embedding Generation (SentenceTransformers)
    ↓
    Vector Database (FAISS - persisted)
    ↓
    Retriever (Top-K similarity search)
    ↓
    LLM (Context-only prompt)
    ↓
    Answer (with session-based memory)

# Key Design Principles

Retrieval-first: The LLM only sees retrieved website content

Strict prompting: Prevents hallucinated answers

Session-only memory: Maintains short-term conversation context

Persistent embeddings: Avoids re-embedding on every query

# AI Frameworks Used
LangChain

    LangChain is used as the orchestration framework to:

    Load website content

    Perform chunking and retrieval

    Integrate embeddings, vector storage, and LLMs

    Build a modular RAG pipeline

    LangGraph was not required since the application does not involve multi-agent workflows or state machines.

# LLM Model Used
Model: google/flan-t5-large

# Why this model was chosen:

    Open-source and free to use

    Instruction-tuned for question answering

    Strong reasoning and summarization ability

    Can be run locally or via HuggingFace pipelines

    No dependency on proprietary APIs

    The model is used strictly in a retrieval-augmented setup, ensuring answers are grounded in website content only.

# Vector Database Used
Vector Store: FAISS

# Why FAISS:

    Fast similarity search

    Lightweight and local

    Ideal for small to medium-scale projects

    No external service dependency

    Easy persistence and reload from disk

    Embeddings are stored locally and reused across sessions, ensuring efficiency.

# Embedding Strategy

    # Embedding Model

    SentenceTransformers (all-MiniLM-L6-v2)

    384-dimensional dense embeddings

# Strategy

    Website content is semantically chunked using spaCy

    Each chunk is converted into an embedding

    Embeddings are stored once in FAISS

    At query time, only similarity search is performed (no re-embedding)

    This provides high semantic recall with low latency.

# Setup and Run Instructions
1. Clone the Repository
git clone https://github.com/ankitchoudhary-bot/Humanli.ai-Project.git
cd Humanli.ai-Project

2. Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

3. Install Dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

4. Run the Streamlit Application
streamlit run app.py

5. Open in Browser

Streamlit will provide a local or public URL where the chatbot UI is accessible.

# Assumptions

    The website contains meaningful textual content

    The website is publicly accessible and does not block scraping

    Single website is indexed per session

    English-language content is assumed

# Limitations

    JavaScript-heavy or dynamically rendered websites may not load fully

    No cross-website querying in a single session

    No advanced relevance thresholding (cosine cutoff)

    Large websites may increase indexing time

    CPU-only inference may be slow for large LLMs

# Future Improvements

    Add multi-page crawling with depth control

    Introduce relevance score thresholds for retrieval

    Support multi-website indexing

    Add source citations per answer

    Implement reranking using cross-encoders

    Deploy with GPU support for faster inference

    Add user authentication and session IDs

    Integrate LangGraph for complex conversational flows

# Public Streamlit Application

👉 Live Demo:
https://humanliai-project-283u67svk9xmbjzifvrdyc.streamlit.app/

# Final Notes

    This project demonstrates:

    End-to-end RAG system design

    Hallucination-safe question answering

    Clean separation of concerns

    Production-aligned architecture

    Evaluator- and interview-friendly implementation