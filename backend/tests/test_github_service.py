from app.services.github_service import parse_github_url


def test_valid_github_url():
    repo = parse_github_url(
        "https://github.com/facebook/react"
    )

    assert repo.owner == "facebook"
    assert repo.name == "react"


def test_valid_github_url_with_trailing_slash():
    repo = parse_github_url(
        "https://github.com/facebook/react/"
    )

    assert repo.owner == "facebook"
    assert repo.name == "react"


def test_valid_git_url():
    repo = parse_github_url(
        "https://github.com/facebook/react.git"
    )

    assert repo.owner == "facebook"
    assert repo.name == "react"


def test_invalid_github_url():
    try:
        parse_github_url("https://google.com/test")
        assert False
    except ValueError:
        assert True


def test_invalid_repository_path():
    try:
        parse_github_url("https://github.com/facebook")
        assert False
    except ValueError:
        assert True