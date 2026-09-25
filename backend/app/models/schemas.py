from typing import Optional

from pydantic import BaseModel


class QueryRequest(BaseModel):

    question: str

    mode: str = "my_document"

    document_id: Optional[str] = None

    top_k: int = 5


class Citation(BaseModel):

    document_id: Optional[str] = None

    document_name: Optional[str] = None

    source_type: Optional[str] = None

    page: Optional[int] = None

    section: Optional[str] = None

    chunk_id: Optional[str] = None

    distance: Optional[float] = None


class QueryResponse(BaseModel):

    answer: str

    citations: list[Citation]

    evaluation: dict
class ComparisonRequest(BaseModel):
    document_a_id: str
    document_b_id: str


class ComparisonResponse(BaseModel):
    document_a_id: str
    document_b_id: str
    answer: str
    document_a_pages: int
    document_b_pages: int