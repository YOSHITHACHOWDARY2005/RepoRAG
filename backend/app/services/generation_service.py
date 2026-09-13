from google import genai
from google.genai import errors

from app.config import settings


client = genai.Client(api_key=settings.gemini_api_key)


def generate_answer(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )

    except errors.ClientError as exc:
        if exc.code == 429:
            raise ValueError(
                "Gemini API quota exceeded. Please try again later."
            ) from exc

        raise

    if not response.text:
        raise ValueError("Gemini returned an empty response")

    return response.text