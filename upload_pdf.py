from app.indexer import index_pdf


print("=== RAGnosis PDF Indexer ===")

pdf_path = input("Enter PDF path: ").strip()

index_pdf(pdf_path)

print("\nPDF indexed successfully!")
print("You can now run: python ask.py")