from langchain_huggingface.llms import HuggingFacePipeline
from transformers import pipeline
from vector_embeddings import load_vector_store
from prompt_template import STRICT_RAG_PROMPT_WITH_MEMORY
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
# Load Vector Store
vector_store = load_vector_store()

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

# LLM
hf_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-large"
)

model = HuggingFacePipeline(pipeline=hf_pipeline)



def format_docs(retrieved_docs):
  context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text

chat_history = []

def get_chat_history(_):
    return "\n".join(
        f"User: {q}\nAssistant: {a}"
        for q, a in chat_history
    )

parallel_chain = RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough(),
    "chat_history": RunnableLambda(get_chat_history)
})

parser = StrOutputParser()

main_chain = parallel_chain | STRICT_RAG_PROMPT_WITH_MEMORY | model | parser

def ask_question(question: str):
    answer = main_chain.invoke(question)

    chat_history.append((question, answer))

    return answer



print(ask_question("Who was Ratan Tata?"))
# # print(ask_question("What was topic we discussed just now?"))

# print(chat_history)

