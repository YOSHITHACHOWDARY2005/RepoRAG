from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AskQuestionRequest(BaseModel):
    question: str


class SourceResponse(BaseModel):
    file_path: str
    language: str
    start_line: int
    end_line: int
    distance: float


class AskQuestionResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]


# Repository schemas

class RepositoryCreateRequest(BaseModel):
    repo_url: str = Field(..., min_length=1)


class RepositoryResponse(BaseModel):
    id: UUID
    repo_url: str
    owner: str
    name: str
    branch: str | None
    status: str
    file_count: int
    chunk_count: int
    error_message: str | None
    created_at: datetime
    updated_at: datetime