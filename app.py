import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from chain import ask_question
from vector_embeddings import create_vector_store, load_vector_store
from web_scraping import scrape_url, ScraperError
from pdf_loader import semantic_spacy_chunking
from save_scrape_data import save_text_to_pdf
# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Website QA Chatbot", layout="centered")

st.title("🌐 Website Question Answering Chatbot")

# -----------------------------
# Session State
# -----------------------------
if "indexed" not in st.session_state:
    st.session_state.indexed = False

if "chat" not in st.session_state:
    st.session_state.chat = []

# -----------------------------
# URL Input
# -----------------------------
st.subheader("1️⃣ Enter Website URL")

url = st.text_input("Website URL", placeholder="https://example.com")

# -----------------------------
# Index Website
# -----------------------------
if st.button("Index Website"):
    if not url:
        st.error("Please enter a valid website URL.")
    else:
        with st.spinner("Scraping and indexing website..."):
            try:
                content = scrape_url(url)
                save_text_to_pdf(
                    text=content,
                    filename="web_scraping_article.pdf"
                )
                print("PDF saved successfully!")
  
            except ScraperError as e:
                print("Error:", e)
            
            loader = PyPDFLoader("web_scraping_article.pdf")
            docs = loader.load()
            semantic_chunks = semantic_spacy_chunking(docs, max_chars=500)

            create_vector_store(semantic_chunks)

            st.session_state.indexed = True
            st.success("Website indexed successfully!")

# -----------------------------
# Chat Interface
# -----------------------------
st.subheader("2️⃣ Ask Questions")

if not st.session_state.indexed:
    st.info("Please index a website first.")
else:
    user_question = st.chat_input("Ask a question about the website")

    if user_question:
        answer = ask_question(user_question)

        st.session_state.chat.append(
            {"question": user_question, "answer": answer}
        )

    # Display chat history
    for msg in st.session_state.chat:
        with st.chat_message("user"):
            st.write(msg["question"])
        with st.chat_message("assistant"):
            st.write(msg["answer"])
