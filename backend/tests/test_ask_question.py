from unittest.mock import patch

from app.database import SessionLocal
from app.models import CodeChunk, Repository
from app.services.rag_pipeline_service import ask_question


def test_ask_question():
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
            return_value="The repository contains Flask application code.",
        ):

            result = ask_question(
                db=db,
                repository_id=repository.id,
                question="What does this repository contain?",
                top_k=5,
            )

        assert result["answer"]
        assert result["sources"]
        assert len(result["sources"]) <= 5

    finally:
        db.close()