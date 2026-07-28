from langchain_core.documents import Document
from dataclasses import dataclass

@dataclass
class VectorSearchResult:
    document: Document
    score: float
    embedding: list[float] | None = None