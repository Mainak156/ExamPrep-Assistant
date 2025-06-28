from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

# Load HuggingFace Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="thenlper/gte-small")

def split_text_into_chunks(text, chunk_size=800, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    docs = splitter.create_documents([text])
    return docs

def create_and_save_vector_store(docs, persist_directory="vector_store"):
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    return vectordb

def load_vector_store(persist_directory="vector_store"):
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )
    return vectordb
