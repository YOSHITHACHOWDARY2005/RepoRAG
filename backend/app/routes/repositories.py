from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Repository
from app.schemas import RepositoryCreateRequest, RepositoryResponse
from app.services.repository_service import ingest_repository


router = APIRouter(
    prefix="/api/repositories",
    tags=["Repositories"],
)


@router.post(
    "",
    response_model=RepositoryResponse,
)
def create_repository(
    request: RepositoryCreateRequest,
    db: Session = Depends(get_db),
):
    try:
        repository = ingest_repository(
            db=db,
            repo_url=request.repo_url,
        )

        return repository

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[RepositoryResponse],
)
def list_repositories(
    db: Session = Depends(get_db),
):
    return (
        db.query(Repository)
        .order_by(Repository.created_at.desc())
        .all()
    )


@router.get(
    "/{repository_id}",
    response_model=RepositoryResponse,
)
def get_repository(
    repository_id: UUID,
    db: Session = Depends(get_db),
):
    repository = (
        db.query(Repository)
        .filter(Repository.id == repository_id)
        .first()
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    return repository


@router.delete(
    "/{repository_id}",
)
def delete_repository(
    repository_id: UUID,
    db: Session = Depends(get_db),
):
    repository = (
        db.query(Repository)
        .filter(Repository.id == repository_id)
        .first()
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    db.delete(repository)
    db.commit()

    return {
        "message": "Repository deleted successfully",
        "repository_id": str(repository_id),
    }