import os

from app.pdf_processor import extract_pages_from_pdf
from app.rag import split_pages_into_chunks
from app.vector_store import create_vector_store, save_vector_store


def index_all_documents(
    documents_path="data/documents",
    vectorstore_path="vectorstore"
):
    print("Reading documents...")

    all_chunks = []

    for filename in os.listdir(documents_path):

        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(documents_path, filename)

        print("Processing:", filename)

        pages = extract_pages_from_pdf(pdf_path)
        chunks = split_pages_into_chunks(pages)

        for chunk in chunks:
            chunk["source"] = filename

        all_chunks.extend(chunks)

    print("Total chunks:", len(all_chunks))

    vector_store = create_vector_store(all_chunks)

    save_vector_store(vector_store, vectorstore_path)

    print("FAISS index saved successfully!")

    return vector_store