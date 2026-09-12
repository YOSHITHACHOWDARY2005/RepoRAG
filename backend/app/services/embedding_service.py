from google import genai

from app.config import settings


client = genai.Client(api_key=settings.gemini_api_key)


def generate_embedding(text: str) -> list[float]:
    response = client.models.embed_content(
        model=settings.embedding_model,
        contents=text,
        config={
            "output_dimensionality": 768
        }
    )

    return response.embeddings[0].values


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    response = client.models.embed_content(
        model=settings.embedding_model,
        contents=texts,
        config={
            "output_dimensionality": 768
        }
    )

    return [
        embedding.values
        for embedding in response.embeddings
    ]