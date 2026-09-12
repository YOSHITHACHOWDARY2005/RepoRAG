from app.services.embedding_service import generate_embedding


def test_generate_embedding():
    text = "This is a test function in a Python repository."

    embedding = generate_embedding(text)

    assert embedding
    assert isinstance(embedding, list)
    assert len(embedding) == 768