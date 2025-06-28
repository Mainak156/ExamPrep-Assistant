from utils.pdf_reader import extract_text_from_pdf
from rag_pipeline.embedder import split_text_into_chunks, create_and_save_vector_store

def process_pdf_to_vector_store(pdf_path):
    print(f"📄 Extracting text from {pdf_path}...")
    text = extract_text_from_pdf(pdf_path)

    print(f"📚 Splitting text into chunks...")
    docs = split_text_into_chunks(text)

    print(f"🔍 Embedding and saving vector store...")
    vectordb = create_and_save_vector_store(docs)

    print(f"✅ Vector store created with {len(docs)} documents.")