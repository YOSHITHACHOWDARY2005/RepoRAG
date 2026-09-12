from app.services.github_service import clone_repository


def test_clone_public_repository():
    repo_url = "https://github.com/octocat/Hello-World"

    repository, clone_path, temp_directory = clone_repository(repo_url)

    try:
        assert repository.owner == "octocat"
        assert repository.name == "Hello-World"
        assert clone_path.exists()
        assert clone_path.is_dir()
    finally:
        temp_directory.cleanup()