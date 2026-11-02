from app.pdf_processor import extract_pages_from_pdf
from app.rag import split_pages_into_chunks
from app.vector_store import create_vector_store



pdf_path = "data/documents/qa_test.pdf"
RELEVANCE_THRESHOLD = 1.3

# 1. Extract pages
pages = extract_pages_from_pdf(pdf_path)

print("Total pages:", len(pages))


# 2. Split pages into chunks
chunks = split_pages_into_chunks(pages)

print("Total chunks:", len(chunks))


# 3. Create FAISS vector store
vector_store = create_vector_store(chunks)

print("FAISS vector store created successfully!")


# 4. Questions for retrieval testing
questions = [
    "What is RAG?",
    "What is Python?",
    "What is machine learning?",
    "What is FAISS?",
    "What is Docker?",
    "What is database normalization?"
]

for question in questions:

    results = vector_store.similarity_search_with_score(
        question,
        k=1
    )

    result, score = results[0]

    print("\n================================")
    print("QUESTION:", question)
    print("SCORE:", round(score, 4))

    if score <= RELEVANCE_THRESHOLD:

        print("STATUS: RELEVANT")
        print("PAGE:", result.metadata["page"])
        print("RETRIEVED TEXT:")
        print(result.page_content[:300])

    else:

        print("STATUS: NOT RELEVANT")