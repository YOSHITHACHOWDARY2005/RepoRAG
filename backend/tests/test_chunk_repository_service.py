from app.database import SessionLocal
from app.models import CodeChunk, Repository
from app.services.chunk_repository_service import chunk_repository


def test_chunk_repository():
    db = SessionLocal()

    try:
        repository = (
            db.query(Repository)
            .filter(
                Repository.repo_url
                == "https://github.com/pallets/flask"
            )
            .first()
        )

        assert repository is not None

        count = chunk_repository(
            db,
            repository.id
        )

        assert count > 0

        chunks = (
            db.query(CodeChunk)
            .filter(
                CodeChunk.repository_id
                == repository.id
            )
            .all()
        )

        assert len(chunks) == count

        first_chunk = chunks[0]

        assert first_chunk.content
        assert first_chunk.start_line >= 1
        assert first_chunk.end_line >= first_chunk.start_line
        assert first_chunk.chunk_metadata is not None

    finally:
        db.close()