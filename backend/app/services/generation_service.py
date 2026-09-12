from google import genai

from app.config import settings


client = genai.Client(api_key=settings.gemini_api_key)


def generate_answer(prompt: str) -> str:
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response")

    return response.text