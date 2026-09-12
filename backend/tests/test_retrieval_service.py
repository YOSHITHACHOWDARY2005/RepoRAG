from app.database import SessionLocal
from app.models import CodeChunk
from app.services.retrieval_service import search_similar_chunks


def test_search_similar_chunks():
    db = SessionLocal()

    try:
        source_chunk = (
            db.query(CodeChunk)
            .filter(CodeChunk.embedding.is_not(None))
            .first()
        )

        assert source_chunk is not None

        results = search_similar_chunks(
            db=db,
            query_embedding=source_chunk.embedding,
            repository_id=source_chunk.repository_id,
            top_k=5,
        )

        assert results
        assert len(results) <= 5

        for result in results:
            assert result.chunk.embedding is not None
            assert result.chunk.repository_id == source_chunk.repository_id
            assert result.file_path
            assert result.language
            assert result.start_line >= 1
            assert result.end_line >= result.start_line
            assert result.distance >= 0

    finally:
        db.close()