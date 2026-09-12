from app.services.retrieval_service import RetrievedChunk


def build_context(retrieved_chunks: list[RetrievedChunk]) -> str:
    if not retrieved_chunks:
        return ""

    context_parts = []

    for index, result in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            f"[Source {index}]\n"
            f"File: {result.file_path}\n"
            f"Language: {result.language}\n"
            f"Lines: {result.start_line}-{result.end_line}\n"
            f"Content:\n"
            f"{result.chunk.content}\n"
        )

    return "\n".join(context_parts)