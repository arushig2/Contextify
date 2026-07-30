from fastapi import APIRouter

from app.models.request import QueryRequest
from app.models.response import QueryResponse
from app.dependencies import rag_chain

router = APIRouter()



@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    answer = rag_chain.invoke(request.question)

    return QueryResponse(answer=answer)