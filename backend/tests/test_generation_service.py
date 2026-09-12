from app.services.generation_service import generate_answer


def test_generate_answer():
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
    assert isinstance(answer, str)
    assert len(answer.strip()) > 0