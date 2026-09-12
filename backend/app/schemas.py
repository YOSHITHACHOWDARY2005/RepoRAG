from pydantic import BaseModel


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