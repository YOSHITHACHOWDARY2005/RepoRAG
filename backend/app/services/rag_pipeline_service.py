from sqlalchemy.orm import Session

from app.services.retrieval_service import search_similar_chunks
from app.services.rag_service import build_context
from app.prompts.rag_prompt import build_rag_prompt
from app.services.generation_service import generate_answer
from app.services.embedding_service import generate_embedding

def run_rag_pipeline(
    db: Session,
    repository_id,
    question: str,
    query_embedding: list[float],
    top_k: int = 5,
) -> dict:

    # Step 1: Retrieve similar chunks
    retrieved_chunks = search_similar_chunks(
        db=db,
        query_embedding=query_embedding,
        repository_id=repository_id,
        top_k=top_k,
    )

    # Step 2: Build context from retrieved chunks
    context = build_context(retrieved_chunks)

    # Step 3: Build grounded Gemini prompt
    prompt = build_rag_prompt(
        question=question,
        context=context,
    )

    # Step 4: Generate answer
    answer = generate_answer(prompt)

    # Step 5: Prepare source information
    sources = []

    for result in retrieved_chunks:
        sources.append(
            {
                "file_path": result.file_path,
                "language": result.language,
                "start_line": result.start_line,
                "end_line": result.end_line,
                "distance": result.distance,
            }
        )

    return {
        "answer": answer,
        "sources": sources,
    }


def ask_question(
    db: Session,
    repository_id,
    question: str,
    top_k: int = 5,
) -> dict:

    query_embedding = generate_embedding(question)

    return run_rag_pipeline(
        db=db,
        repository_id=repository_id,
        question=question,
        query_embedding=query_embedding,
        top_k=top_k,
    )