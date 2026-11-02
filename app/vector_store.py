from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def create_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vector_store(chunks):

    embedding_model = create_embedding_model()

    texts = []
    metadatas = []

    for chunk in chunks:

        texts.append(chunk["text"])

        metadatas.append({
            "page": chunk["page"],
            "source": chunk.get("source", "unknown")
        })

    return FAISS.from_texts(
        texts,
        embedding_model,
        metadatas=metadatas
    )


def save_vector_store(vector_store, path):
    vector_store.save_local(path)


def load_vector_store(path):

    embedding_model = create_embedding_model()

    return FAISS.load_local(
        path,
        embedding_model,
        allow_dangerous_deserialization=True
    )