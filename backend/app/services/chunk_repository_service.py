from sqlalchemy.orm import Session
from sqlalchemy import delete
from app.models import CodeChunk, Repository
from app.services.chunking_service import chunk_text
from app.services.file_filter_service import get_supported_files
from app.services.file_reader_service import read_file_content
from app.services.github_service import clone_repository


def chunk_repository(
    db: Session,
    repository_id,
) -> int:

    repository = db.get(Repository, repository_id)

    if repository is None:
        raise ValueError("Repository not found")
    
    
    db.execute(
        delete(CodeChunk).where(
            CodeChunk.repository_id == repository.id
            )
    )
    db.flush()



    github_repo, repo_path, temp_directory = clone_repository(
        repository.repo_url
    )

    try:
        files = get_supported_files(repo_path)

        total_chunks = 0

        for file_path in files:
            relative_path = str(
                file_path.relative_to(repo_path)
            ).replace("\\", "/")

            repository_file = next(
                (
                    file
                    for file in repository.files
                    if file.file_path == relative_path
                ),
                None,
            )

            if repository_file is None:
                continue

            content = read_file_content(file_path)

            chunks = chunk_text(
                content,
                chunk_size=80,
                overlap=20,
            )

            for chunk in chunks:
                code_chunk = CodeChunk(
                    repository_id=repository.id,
                    file_id=repository_file.id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    start_line=chunk.start_line,
                    end_line=chunk.end_line,
                    chunk_metadata={
                        "file_path": relative_path,
                        "language": repository_file.language,
                    },
                )

                db.add(code_chunk)
                total_chunks += 1

        repository.chunk_count = total_chunks

        db.commit()

        return total_chunks

    except Exception:
        db.rollback()
        raise

    finally:
        temp_directory.cleanup()