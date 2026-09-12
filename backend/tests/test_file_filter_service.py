from pathlib import Path

from app.services.file_filter_service import (
    is_supported_file,
    should_ignore_path,
)


def test_supported_python_file(tmp_path):
    file_path = tmp_path / "main.py"
    file_path.write_text("print('hello')")

    assert is_supported_file(file_path) is True


def test_supported_typescript_file(tmp_path):
    file_path = tmp_path / "app.tsx"
    file_path.write_text("export default function App() {}")

    assert is_supported_file(file_path) is True


def test_unsupported_file(tmp_path):
    file_path = tmp_path / "image.png"
    file_path.write_bytes(b"fake image")

    assert is_supported_file(file_path) is False


def test_env_file_is_ignored(tmp_path):
    file_path = tmp_path / ".env"
    file_path.write_text("SECRET=123")

    assert is_supported_file(file_path) is False


def test_node_modules_is_ignored():
    path = Path("project/node_modules/package/index.js")

    assert should_ignore_path(path) is True


def test_git_directory_is_ignored():
    path = Path("project/.git/config")

    assert should_ignore_path(path) is True


def test_venv_directory_is_ignored():
    path = Path("project/.venv/lib/python/site.py")

    assert should_ignore_path(path) is True