from sqlalchemy.orm import Session

from app.models import Repository
from app.services.repository_service import ingest_repository
from app.services.chunk_repository_service import chunk_repository
from app.services.embedding_repository_service import embed_all_chunks


def process_repository(
    db: Session,
    repo_url: str,
) -> Repository:

    existing_repository = (
        db.query(Repository)
        .filter(Repository.repo_url == repo_url)
        .first()
    )

    if existing_repository is not None:
        if (
            existing_repository.chunk_count > 0
            and existing_repository.status == "completed"
        ):
            return existing_repository

        repository = existing_repository

    else:
        repository = ingest_repository(
            db=db,
            repo_url=repo_url,
        )

    repository.status = "processing"
    db.commit()
    db.refresh(repository)

    chunk_count = chunk_repository(
        db=db,
        repository_id=repository.id,
    )

    embedded_count = embed_all_chunks(
        db=db,
        repository_id=repository.id,
    )

    if embedded_count == chunk_count:
        repository.status = "completed"
    else:
        repository.status = "embedding_pending"

    repository.chunk_count = chunk_count

    db.commit()
    db.refresh(repository)

    return repository