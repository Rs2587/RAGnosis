from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os


from app.vector_store import load_vector_store
from app.llm import generate_answer
from app.indexer import index_all_documents


app = FastAPI(
    title="RAGnosis API",
    description="Document Question Answering API",
    version="1.0"
)
app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)


@app.get("/app")
def frontend():
    return FileResponse("frontend/index.html")


# Load existing FAISS index
vector_store = load_vector_store("vectorstore")


# Lower FAISS distance = more relevant
RELEVANCE_THRESHOLD = 1.85


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():

    return {
        "message": "RAGnosis API is running"
    }


@app.get("/documents")
def get_documents():

    documents_path = "data/documents"

    documents = []

    if os.path.exists(documents_path):

        for filename in os.listdir(documents_path):

            if filename.lower().endswith(".pdf"):
                documents.append(filename)

    return {
        "total_documents": len(documents),
        "documents": documents
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    results = vector_store.similarity_search_with_score(
        question,
        k=3
    )

    relevant_results = []

    for result, score in results:

        if score <= RELEVANCE_THRESHOLD:

            relevant_results.append(
                (result, score)
            )

    if not relevant_results:

        return {
            "answer": "I could not find the answer in the provided document.",
            "sources": []
        }

    context = "\n\n".join(
        result.page_content
        for result, score in relevant_results
    )

    answer = generate_answer(
        question,
        context
    )

    sources = []

    for result, score in relevant_results:

        sources.append({
            "document": result.metadata.get(
                "source",
                "unknown"
            ),
            "page": result.metadata.get(
                "page",
                "unknown"
            ),
            "score": round(float(score), 4)
        })

    return {
        "answer": answer,
        "sources": sources
    }


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    global vector_store

    # Check file extension
    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    documents_path = "data/documents"

    os.makedirs(
        documents_path,
        exist_ok=True
    )

    # Prevent unsafe filenames
    filename = os.path.basename(file.filename)

    pdf_path = os.path.join(
        documents_path,
        filename
    )

    # Save uploaded file
    with open(pdf_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Basic PDF validation
    with open(pdf_path, "rb") as pdf_file:

        header = pdf_file.read(4)

    if header != b"%PDF":

        os.remove(pdf_path)

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid PDF."
        )

    # Rebuild FAISS index
    vector_store = index_all_documents()

    total_documents = len([
        f
        for f in os.listdir(documents_path)
        if f.lower().endswith(".pdf")
    ])

    return {
        "message": "PDF uploaded and indexed successfully.",
        "filename": filename,
        "total_documents": total_documents
    }


@app.delete("/documents/{filename}")
def delete_document(filename: str):

    global vector_store

    documents_path = "data/documents"

    filename = os.path.basename(filename)

    pdf_path = os.path.join(
        documents_path,
        filename
    )

    if not filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF documents can be deleted."
        )

    if not os.path.exists(pdf_path):

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    # Find current PDFs
    documents = [
        f
        for f in os.listdir(documents_path)
        if f.lower().endswith(".pdf")
    ]

    # Don't allow an empty vector store
    if len(documents) <= 1:

        raise HTTPException(
            status_code=400,
            detail="Cannot delete the last document."
        )

    # Delete PDF
    os.remove(pdf_path)

    # Rebuild FAISS index
    vector_store = index_all_documents()

    return {
        "message": "Document deleted successfully.",
        "deleted_document": filename,
        "remaining_documents": len(documents) - 1
    }