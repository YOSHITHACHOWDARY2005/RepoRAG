from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AskQuestionRequest, AskQuestionResponse
from app.services.rag_pipeline_service import ask_question


router = APIRouter(
    prefix="/api/repositories",
    tags=["RAG"],
)


@router.post(
    "/{repository_id}/ask",
    response_model=AskQuestionResponse,
)
def ask_repository_question(
    repository_id: UUID,
    request: AskQuestionRequest,
    db: Session = Depends(get_db),
):
    return ask_question(
        db=db,
        repository_id=repository_id,
        question=request.question,
    )