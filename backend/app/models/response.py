from pydantic import BaseModel

class Citation(BaseModel):
    source: str
    source_type: str | None = None

class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]

class IngestionResponse(BaseModel):
    message: str
    documents: int
    chunks: int