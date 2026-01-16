from langchain_community.document_loaders import PyPDFLoader
import spacy
from langchain_classic.schema import Document
# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def semantic_spacy_chunking(docs, max_chars=500):
    """
    Semantic chunking using spaCy sentence boundaries.
    Preserves metadata and avoids mid-sentence splits.
    """
    chunks = []

    for doc in docs:
        sentences = [sent.text.strip() for sent in nlp(doc.page_content).sents]

        current_chunk = ""
        for sent in sentences:
            # If adding sentence stays within limit → append
            if len(current_chunk) + len(sent) <= max_chars:
                current_chunk += " " + sent
            else:
                # Save chunk
                chunks.append(
                    Document(
                        page_content=current_chunk.strip(),
                        metadata=doc.metadata
                    )
                )
                current_chunk = sent

        # Add leftover text
        if current_chunk:
            chunks.append(
                Document(
                    page_content=current_chunk.strip(),
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
