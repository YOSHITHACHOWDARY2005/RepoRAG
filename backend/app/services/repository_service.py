from pathlib import Path

from sqlalchemy.orm import Session

from app.models import Repository, RepositoryFile
from app.services.file_reader_service import get_file_metadata
from app.services.file_filter_service import get_supported_files
from app.services.github_service import clone_repository


EXTENSION_TO_LANGUAGE = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".h": "c",
    ".hpp": "cpp",
    ".go": "go",
    ".rs": "rust",
    ".md": "markdown",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".sql": "sql",
    ".html": "html",
    ".css": "css",
}


def detect_language(file_path: Path) -> str:
    return EXTENSION_TO_LANGUAGE.get(
        file_path.suffix.lower(),
        "text"
    )


def ingest_repository(
    db: Session,
    repo_url: str
) -> Repository:

    github_repo = None
    temp_directory = None

    try:
        github_repo, repo_path, temp_directory = clone_repository(repo_url)

        repository = Repository(
            repo_url=github_repo.url,
            owner=github_repo.owner,
            name=github_repo.name,
            branch="main",
            status="processing",
        )

        db.add(repository)
        db.commit()
        db.refresh(repository)

        files = get_supported_files(repo_path)

        for file_path in files:
            metadata = get_file_metadata(
                file_path,
                repo_path
            )

            repository_file = RepositoryFile(
                repository_id=repository.id,
                file_path=metadata["file_path"],
                language=detect_language(file_path),
                content_hash=metadata["content_hash"],
                file_size=metadata["file_size"],
            )

            db.add(repository_file)

        repository.file_count = len(files)
        repository.status = "completed"

        db.commit()
        db.refresh(repository)

        return repository

    except Exception as exc:
        db.rollback()
        raise exc

    finally:
        if temp_directory is not None:
            temp_directory.cleanup()