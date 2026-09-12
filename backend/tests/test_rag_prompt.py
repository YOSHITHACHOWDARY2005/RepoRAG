from app.prompts.rag_prompt import build_rag_prompt


def test_build_rag_prompt():
    question = "How does this repository handle routing?"
    context = """
[Source 1]
File: app/routes.py
Language: python
Lines: 10-25
Content:
@app.get("/users")
def get_users():
    return users
"""

    prompt = build_rag_prompt(question, context)

    assert question in prompt
    assert context.strip() in prompt
    assert "ONLY" in prompt
    assert "[Source N]" in prompt
    assert "Do not invent" in prompt