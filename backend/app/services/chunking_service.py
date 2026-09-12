from dataclasses import dataclass


@dataclass
class TextChunk:
    content: str
    start_line: int
    end_line: int
    chunk_index: int


def chunk_text(
    content: str,
    chunk_size: int = 80,
    overlap: int = 20,
) -> list[TextChunk]:

    if not content.strip():
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    lines = content.splitlines()

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(lines):
        end = min(
            start + chunk_size,
            len(lines)
        )

        chunk_content = "\n".join(
            lines[start:end]
        )

        chunks.append(
            TextChunk(
                content=chunk_content,
                start_line=start + 1,
                end_line=end,
                chunk_index=chunk_index,
            )
        )

        if end == len(lines):
            break

        start = end - overlap
        chunk_index += 1

    return chunks