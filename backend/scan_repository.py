from app.services.ingestion_service import scan_repository


repo_url = "https://github.com/pallets/flask"

files, temp_directory = scan_repository(repo_url)

try:
    print(f"\nFound {len(files)} supported files:\n")

    for file_path in files:
        print(file_path)

finally:
    temp_directory.cleanup()