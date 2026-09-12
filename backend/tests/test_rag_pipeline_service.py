from app.database import SessionLocal
from app.models import CodeChunk, Repository
from app.services.rag_pipeline_service import run_rag_pipeline


def test_run_rag_pipeline():
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

        fake_answer = (
            "The repository contains Flask application code."
        )

        from unittest.mock import patch

        with patch(
            "app.services.rag_pipeline_service.generate_answer",
            return_value=fake_answer,
        ):
            result = run_rag_pipeline(
                db=db,
                repository_id=repository.id,
                question="What does this repository contain?",
                query_embedding=list(chunk.embedding),
                top_k=5,
            )

        assert result["answer"] == fake_answer
        assert "sources" in result
        assert len(result["sources"]) > 0

        source = result["sources"][0]

        assert source["file_path"]
        assert source["language"]
        assert source["start_line"] >= 1
        assert source["end_line"] >= source["start_line"]
        assert source["distance"] >= 0

    finally:
        db.close()