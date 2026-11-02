from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json()["message"] == "RAGnosis API is running"


def test_documents():
    response = client.get("/documents")

    assert response.status_code == 200

    data = response.json()

    assert "total_documents" in data
    assert "documents" in data


def test_empty_question():
    response = client.post(
        "/ask",
        json={"question": ""}
    )

    assert response.status_code == 400