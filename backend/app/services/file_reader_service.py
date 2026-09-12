from pathlib import Path
import hashlib


def read_file_content(file_path: Path) -> str:
    return file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def calculate_content_hash(content: str) -> str:
    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def get_file_metadata(file_path: Path, repository_root: Path) -> dict:
    content = read_file_content(file_path)

    relative_path = file_path.relative_to(repository_root)

    return {
        "file_path": str(relative_path).replace("\\", "/"),
        "file_size": file_path.stat().st_size,
        "content": content,
        "content_hash": calculate_content_hash(content),
    }