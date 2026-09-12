from app.services.ingestion_service import scan_repository


def test_scan_real_repository():
    repo_url = "https://github.com/pallets/flask"
    files, temp_directory = scan_repository(repo_url)

    try:
        assert len(files) > 0

        for file_path in files:
            assert file_path.is_file()
            assert ".git" not in file_path.parts
            assert "node_modules" not in file_path.parts

    finally:
        temp_directory.cleanup()