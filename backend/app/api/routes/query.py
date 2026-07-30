from fastapi import APIRouter

from app.models.request import QueryRequest
from app.models.response import QueryResponse
from app.dependencies import rag_chain
from app.utils.citations import extract_citations

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    result = rag_chain.invoke(request.question)
    citations = extract_citations(result["documents"])
    return QueryResponse(
        answer=result["answer"],
        citations=citations,
    )