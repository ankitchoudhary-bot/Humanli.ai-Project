from langchain_core.documents import Document
import re

def semantic_chunking(docs, max_chars=500):
    """
    Sentence-aware chunking without spaCy
    """
    chunks = []

    for doc in docs:
        sentences = re.split(r'(?<=[.!?])\s+', doc.page_content)
        buffer = ""

        for sent in sentences:
            if len(buffer) + len(sent) <= max_chars:
                buffer += " " + sent
            else:
                chunks.append(
                    Document(
                        page_content=buffer.strip(),
                        metadata=doc.metadata
                    )
                )
                buffer = sent

        if buffer.strip():
            chunks.append(
                Document(
                    page_content=buffer.strip(),
                    metadata=doc.metadata
                )
            )

    return chunks


# if __name__ == "__main__":
#     loader = PyPDFLoader("web_scraping_article.pdf")
#     docs = loader.load()

#     semantic_chunks = semantic_spacy_chunking(docs, max_chars=500)

#     print(f"Total semantic chunks: {len(semantic_chunks)}")
#     print(semantic_chunks[0].page_content)
#     print(semantic_chunks[0].metadata)
