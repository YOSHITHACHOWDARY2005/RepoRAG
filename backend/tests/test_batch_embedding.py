from app.database import SessionLocal
from app.models import CodeChunk
from app.services.embedding_service import generate_embeddings


def test_generate_and_store_small_batch():
    db = SessionLocal()

    try:
        chunks = (
            db.query(CodeChunk)
            .filter(CodeChunk.embedding.is_(None))
            .limit(3)
            .all()
        )

        assert len(chunks) == 3

        texts = [chunk.content for chunk in chunks]

        embeddings = generate_embeddings(texts)

        assert len(embeddings) == 3

        for chunk, embedding in zip(chunks, embeddings):
            assert len(embedding) == 768

            chunk.embedding = embedding

        db.commit()

    finally:
        db.close()