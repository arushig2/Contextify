from pydantic import BaseModel


class QueryResponse(BaseModel):
    answer: str

class IngestionResponse(BaseModel):
    message: str
    documents: int
    chunks: int