from app.services.embedding_service import generate_embeddings


def test_generate_embeddings():
    texts = [
        "Python function that calculates a sum.",
        "FastAPI route for retrieving repository information.",
        "PostgreSQL database connection configuration.",
    ]

    embeddings = generate_embeddings(texts)

    assert len(embeddings) == len(texts)

    for embedding in embeddings:
        assert isinstance(embedding, list)
        assert len(embedding) == 768