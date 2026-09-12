from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models import CodeChunk


@dataclass
class RetrievedChunk:
    chunk: CodeChunk
    file_path: str
    language: str
    start_line: int
    end_line: int
    distance: float


def search_similar_chunks(
    db: Session,
    query_embedding: list[float],
    repository_id,
    top_k: int = 5,
) -> list[RetrievedChunk]:

    distance = CodeChunk.embedding.cosine_distance(query_embedding)

    results = (
        db.query(CodeChunk, distance)
        .filter(
            CodeChunk.repository_id == repository_id,
            CodeChunk.embedding.is_not(None),
        )
        .order_by(distance)
        .limit(top_k)
        .all()
    )

    retrieved_chunks = []

    for chunk, chunk_distance in results:
        metadata = chunk.chunk_metadata or {}

        retrieved_chunks.append(
            RetrievedChunk(
                chunk=chunk,
                file_path=metadata.get("file_path", "unknown"),
                language=metadata.get("language", "text"),
                start_line=chunk.start_line,
                end_line=chunk.end_line,
                distance=float(chunk_distance),
            )
        )

    return retrieved_chunks