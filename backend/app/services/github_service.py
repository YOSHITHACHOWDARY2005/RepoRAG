import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from git import Repo
from git.exc import GitCommandError


@dataclass
class GitHubRepository:
    owner: str
    name: str
    url: str


GITHUB_URL_PATTERN = re.compile(
    r"^https?://github\.com/"
    r"(?P<owner>[A-Za-z0-9_.-]+)/"
    r"(?P<repo>[A-Za-z0-9_.-]+)"
    r"/?$"
)


def parse_github_url(repo_url: str) -> GitHubRepository:
    """
    Validate a public GitHub repository URL and extract
    the owner and repository name.
    """

    repo_url = repo_url.strip()

    match = GITHUB_URL_PATTERN.match(repo_url)

    if not match:
        raise ValueError(
            "Invalid GitHub repository URL. "
            "Use a URL such as https://github.com/owner/repository"
        )

    owner = match.group("owner")
    name = match.group("repo")

    if name.endswith(".git"):
        name = name[:-4]

    if not owner or not name:
        raise ValueError(
            "GitHub owner and repository name are required."
        )

    normalized_url = f"https://github.com/{owner}/{name}"

    return GitHubRepository(
        owner=owner,
        name=name,
        url=normalized_url,
    )


def clone_repository(
    repo_url: str,
) -> tuple[GitHubRepository, Path, tempfile.TemporaryDirectory]:
    """
    Clone a public GitHub repository into a temporary directory.

    The caller is responsible for keeping the returned TemporaryDirectory
    object alive while using the cloned repository.
    """

    repository = parse_github_url(repo_url)

    temp_directory = tempfile.TemporaryDirectory(
        prefix="reporag_"
    )

    clone_path = Path(temp_directory.name) / repository.name

    try:
        Repo.clone_from(
            repository.url,
            clone_path,
            depth=1,
        )
    except GitCommandError as exc:
        temp_directory.cleanup()

        raise RuntimeError(
            f"Failed to clone repository: {repository.url}"
        ) from exc

    return repository,clone_path, temp_directory