from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str

class IngestionRequest(BaseModel):
    source: str
    loader: str
    chunker: str = "recursive"