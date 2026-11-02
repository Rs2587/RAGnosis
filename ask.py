from app.vector_store import load_vector_store
from app.llm import generate_answer


vectorstore_path = "vectorstore"

RELEVANCE_THRESHOLD = 1.3


# 1. Load saved FAISS vector store
vector_store = load_vector_store(vectorstore_path)

print("RAGnosis is ready!")
print("Type 'exit' to quit.")


# 2. Continuous question loop
while True:

    question = input("\nEnter your question: ")

    # 3. Exit condition
    if question.lower() == "exit":
        print("Exiting RAGnosis...")
        break

    # 4. Search FAISS
    results = vector_store.similarity_search_with_score(
        question,
        k=1
    )

    # 5. Filter relevant results
    relevant_results = []

    for result, score in results:

        if score <= RELEVANCE_THRESHOLD:
            relevant_results.append((result, score))

    # 6. Check relevance
    if not relevant_results:

        print("\n--- FINAL ANSWER ---")
        print("I could not find the answer in the provided document.")
        continue

    # 7. Build context
    context = "\n\n".join(
        result.page_content
        for result, score in relevant_results
    )

    print("\n--- RETRIEVED CONTEXT ---")
    print(context)

    # 8. Generate answer
    answer = generate_answer(
        question,
        context
    )

    print("\n--- FINAL ANSWER ---")
    print(answer)

    # 9. Show source
    print("\n--- SOURCES ---")

    for result, score in relevant_results:

        print("Document: data/documents/qa_test.pdf")
        print("Page:", result.metadata["page"])
        print("Similarity score:", round(score, 4))