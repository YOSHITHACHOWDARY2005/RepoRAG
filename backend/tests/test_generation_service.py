from app.services.generation_service import generate_answer


class MockResponse:
    text = "The function used to calculate the sum is calculate_sum."


def test_generate_answer(monkeypatch):
    def mock_generate_content(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(
        "app.services.generation_service.client.models.generate_content",
        mock_generate_content,
    )

    prompt = """
You are RepoRAG.

Answer the question using only the provided context.

Question:
What function is used to calculate the sum?

Context:
[Source 1]
File: app/example.py
Lines: 1-5

def calculate_sum(a, b):
    return a + b
""".strip()

    answer = generate_answer(prompt)

    assert answer
    assert "calculate_sum" in answer