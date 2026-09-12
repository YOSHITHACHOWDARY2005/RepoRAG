from pathlib import Path

from app.services.file_filter_service import get_supported_files
from app.services.github_service import clone_repository


def scan_repository(repo_url: str) -> tuple[list[Path], object]:
    """
    Clone a repository and return the files that are safe to index.

    The returned temporary directory must remain alive while
    the returned file paths are being used.
    """

    _,repo_path, temp_directory = clone_repository(repo_url)

    files = get_supported_files(repo_path)

    return files, temp_directory