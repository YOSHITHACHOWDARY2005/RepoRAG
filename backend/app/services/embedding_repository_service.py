from sqlalchemy.orm import Session

from app.models import CodeChunk
from google.genai.errors import ClientError
from app.services.embedding_service import (
    generate_embedding,
    generate_embeddings,
)

def embed_chunk(db: Session, chunk_id) -> CodeChunk:
    chunk = db.get(CodeChunk, chunk_id)

    if chunk is None:
        raise ValueError("Code chunk not found")

    embedding = generate_embedding(chunk.content)

    if len(embedding) != 768:
        raise ValueError(
            f"Expected 768-dimensional embedding, got {len(embedding)}"
        )

    chunk.embedding = embedding

    db.commit()
    db.refresh(chunk)

    return chunk
def embed_all_chunks(db: Session, batch_size: int = 10) -> int:
    total_embedded = 0

    while True:
        chunks = (
            db.query(CodeChunk)
            .filter(CodeChunk.embedding.is_(None))
            .limit(batch_size)
            .all()
        )

        if not chunks:
            break

        texts = [chunk.content for chunk in chunks]

        try:
            embeddings = generate_embeddings(texts)

        except ClientError as exc:
            if exc.code == 429:
                print("Gemini quota exceeded.")
                print(f"Embedded {total_embedded} chunks in this run.")
                print("Run this script again when the quota is available.")
                break

            raise

        if len(embeddings) != len(chunks):
            raise ValueError(
                "Number of embeddings does not match number of chunks"
            )

        for chunk, embedding in zip(chunks, embeddings):
            if len(embedding) != 768:
                raise ValueError(
                    f"Expected 768-dimensional embedding, got {len(embedding)}"
                )

            chunk.embedding = embedding

        db.commit()

        total_embedded += len(chunks)

        print(f"Embedded {total_embedded} chunks in this run.")

    return total_embedded