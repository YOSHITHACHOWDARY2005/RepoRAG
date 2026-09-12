from app.services.rag_service import build_context
from app.services.retrieval_service import RetrievedChunk


def test_build_context():
    retrieved_chunks = [
        RetrievedChunk(
            chunk=None,
            file_path="src/example.py",
            language="python",
            start_line=10,
            end_line=20,
            distance=0.15,
        ),
        RetrievedChunk(
            chunk=None,
            file_path="README.md",
            language="markdown",
            start_line=1,
            end_line=8,
            distance=0.20,
        ),
    ]

    retrieved_chunks[0].chunk = type(
        "MockChunk",
        (),
        {"content": "def hello():\n    return 'Hello'"}
    )()

    retrieved_chunks[1].chunk = type(
        "MockChunk",
        (),
        {"content": "# Example Repository"}
    )()

    context = build_context(retrieved_chunks)

    assert "[Source 1]" in context
    assert "src/example.py" in context
    assert "Lines: 10-20" in context
    assert "def hello()" in context

    assert "[Source 2]" in context
    assert "README.md" in context
    assert "# Example Repository" in context