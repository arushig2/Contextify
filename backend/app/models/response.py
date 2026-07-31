from pydantic import BaseModel

class Citation(BaseModel):
    source: str
    source_type: str | None = None

class QueryMetrics(BaseModel):
    generation_ms: float
    total_ms: float

class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    metrics: QueryMetrics

class IngestionResponse(BaseModel):
    message: str
    documents: int
    chunks: int