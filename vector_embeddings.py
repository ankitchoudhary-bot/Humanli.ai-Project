import os
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_DB_PATH = "vector_store/faiss_index"

# Embedding Model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create & Persist Vector DB
def create_vector_store(chunks):
    """
    Create FAISS index from chunks and persist to disk.
    """
    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    vector_store.save_local(VECTOR_DB_PATH)
    print("Vector store created & saved")

# Load Existing Vector DB
def load_vector_store():
    """
    Load FAISS index from disk (NO re-embedding).
    """
    if not os.path.exists(VECTOR_DB_PATH):
        raise FileNotFoundError("Vector store not found. Run ingestion first.")

    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings=embedding_model,
        allow_dangerous_deserialization=True
    )


# from pdf_loader import semantic_spacy_chunking
# from langchain_community.document_loaders import PyPDFLoader

# loader = PyPDFLoader("web_scraping_article.pdf")
# docs = loader.load()

# chunks = semantic_spacy_chunking(docs)

# create_vector_store(chunks)

# vector_store = load_vector_store()

# retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# results=retriever.invoke('What is web scraping?')

# for res in results:
#     print(res.page_content)
#     # print(res.metadata)
