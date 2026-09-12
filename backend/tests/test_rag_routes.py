from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.database import SessionLocal
from app.models import Repository, CodeChunk


client = TestClient(app)


def test_ask_repository_question():
    db = SessionLocal()

    try:
        repository = (
            db.query(Repository)
            .filter(Repository.name == "flask")
            .first()
        )

        assert repository is not None

        chunk = (
            db.query(CodeChunk)
            .filter(
                CodeChunk.repository_id == repository.id,
                CodeChunk.embedding.is_not(None),
            )
            .first()
        )

        assert chunk is not None

        fake_embedding = list(chunk.embedding)

        with patch(
            "app.services.rag_pipeline_service.generate_embedding",
            return_value=fake_embedding,
        ), patch(
            "app.services.rag_pipeline_service.generate_answer",
            return_value="This is a test RAG answer.",
        ):

            response = client.post(
                f"/api/repositories/{repository.id}/ask",
                json={
                    "question": "What does this repository contain?"
                },
            )

        assert response.status_code == 200

        data = response.json()

        assert data["answer"] == "This is a test RAG answer."
        assert "sources" in data
        assert len(data["sources"]) > 0

        source = data["sources"][0]

        assert source["file_path"]
        assert source["language"]
        assert source["start_line"] >= 1
        assert source["end_line"] >= source["start_line"]

    finally:
        db.close()