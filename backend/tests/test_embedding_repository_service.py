from app.database import SessionLocal
from app.models import CodeChunk
from app.services.embedding_repository_service import embed_chunk


def test_embed_one_chunk():
    db = SessionLocal()

    try:
        chunk = db.query(CodeChunk).first()

        assert chunk is not None

        updated_chunk = embed_chunk(db, chunk.id)

        assert updated_chunk.embedding is not None
        assert len(updated_chunk.embedding) == 768

    finally:
        db.close()