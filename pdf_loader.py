from langchain_community.document_loaders import PyPDFLoader
import spacy
from langchain_classic.schema import Document
from langchain_core.documents import Document

_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp

def semantic_spacy_chunking(docs, max_chars=500):
    nlp = get_nlp()
    chunks = []

    for doc in docs:
        spacy_doc = nlp(doc.page_content)
        current = ""

        for sent in spacy_doc.sents:
            if len(current) + len(sent.text) <= max_chars:
                current += " " + sent.text
            else:
                chunks.append(Document(page_content=current.strip(), metadata=doc.metadata))
                current = sent.text

        if current.strip():
            chunks.append(Document(page_content=current.strip(), metadata=doc.metadata))

    return chunks

# if __name__ == "__main__":
#     loader = PyPDFLoader("web_scraping_article.pdf")
#     docs = loader.load()

#     semantic_chunks = semantic_spacy_chunking(docs, max_chars=500)

#     print(f"Total semantic chunks: {len(semantic_chunks)}")
#     print(semantic_chunks[0].page_content)
#     print(semantic_chunks[0].metadata)
