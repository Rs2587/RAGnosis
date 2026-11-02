# RAGnosis

## AI-Powered Document Question Answering System

RAGnosis is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their contents.

The system retrieves relevant information from the uploaded documents and uses a locally running Llama 3.2 model to generate grounded answers.

---

## Features

- Upload PDF documents
- Extract text from PDFs
- Question-aware document chunking
- Semantic embeddings using Sentence Transformers
- FAISS vector similarity search
- Relevance filtering
- Local LLM inference using Ollama
- Llama 3.2 integration
- Multi-document question answering
- Source document identification
- Page number and similarity score
- Delete documents
- Automatic FAISS re-indexing
- FastAPI REST API
- Interactive Swagger documentation
- Web-based frontend

---

## Architecture

```text
                 PDF Documents
                      |
                      v
                 PyMuPDF
                      |
                      v
              Text Extraction
                      |
                      v
             Document Chunking
                      |
                      v
           Sentence Transformer
               Embeddings
                      |
                      v
                  FAISS
             Vector Database
                      |
                      |
User Question ------+
                      |
                      v
             Similarity Search
                      |
                      v
            Relevance Filtering
                      |
                      v
            Retrieved Context
                      |
                      v
             Llama 3.2 / Ollama
                      |
                      v
              Grounded Answer
                      |
                      v
        Answer + Source + Page + Score