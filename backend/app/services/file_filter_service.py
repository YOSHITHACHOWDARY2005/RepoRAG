from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".go",
    ".rs",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".sql",
    ".html",
    ".css",
}


IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    "coverage",
    ".next",
}


IGNORED_FILE_NAMES = {
    ".env",
    ".env.local",
    ".env.development",
    ".env.production",
    ".env.test",
}


MAX_FILE_SIZE = 500 * 1024  # 500 KB


def is_supported_file(path: Path) -> bool:
    """
    Check whether a file should be indexed.
    """

    if not path.is_file():
        return False

    if path.name in IGNORED_FILE_NAMES:
        return False

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return False

    if path.stat().st_size > MAX_FILE_SIZE:
        return False

    return True


def should_ignore_path(path: Path) -> bool:
    """
    Check whether a path is inside an ignored directory.
    """

    return any(
        part in IGNORED_DIRECTORIES
        for part in path.parts
    )


def get_supported_files(repo_path: Path) -> list[Path]:
    """
    Recursively find files that are safe and supported for indexing.
    """

    supported_files = []

    for path in repo_path.rglob("*"):
        if should_ignore_path(path):
            continue

        if is_supported_file(path):
            supported_files.append(path)

    return supported_files