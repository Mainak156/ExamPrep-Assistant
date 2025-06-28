from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

embedding_model = HuggingFaceEmbeddings(model_name="thenlper/gte-small")

def load_vector_store(persist_directory="vector_store"):
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )
    return vectordb

def close_vector_store(vectordb):
    if vectordb is not None:
        try:
            vectordb._client.close()
        except Exception as e:
            print(f"❌ Error closing vector store: {e}")

def retrieve_context(topic, vectordb, k=5):
    docs = vectordb.similarity_search(topic, k=k)
    filtered_docs = [doc for doc in docs if topic.lower() in doc.page_content.lower()]
    return filtered_docs if filtered_docs else docs
