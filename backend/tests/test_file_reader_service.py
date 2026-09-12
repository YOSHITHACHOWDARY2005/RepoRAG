from pathlib import Path

from app.services.file_reader_service import (
    read_file_content,
    calculate_content_hash,
    get_file_metadata,
)


def test_read_file_content(tmp_path):
    file_path = tmp_path / "example.py"

    file_path.write_text(
        "print('Hello RepoRAG')",
        encoding="utf-8"
    )

    content = read_file_content(file_path)

    assert content == "print('Hello RepoRAG')"


def test_content_hash_is_consistent():
    content = "Hello RepoRAG"

    hash1 = calculate_content_hash(content)
    hash2 = calculate_content_hash(content)

    assert hash1 == hash2
    assert len(hash1) == 64


def test_get_file_metadata(tmp_path):
    repository_root = tmp_path / "repo"
    repository_root.mkdir()

    file_path = repository_root / "src" / "main.py"
    file_path.parent.mkdir()

    file_path.write_text(
        "print('hello')",
        encoding="utf-8"
    )

    metadata = get_file_metadata(
        file_path,
        repository_root
    )

    assert metadata["file_path"] == "src/main.py"
    assert metadata["file_size"] > 0
    assert metadata["content"] == "print('hello')"
    assert len(metadata["content_hash"]) == 64