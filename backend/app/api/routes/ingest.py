from fastapi import APIRouter

from app.models.request import IngestionRequest
from app.models.response import IngestionResponse
from app.dependencies import ingestion_service


router = APIRouter()


@router.post("/ingest", response_model=IngestionResponse)
def ingest(request: IngestionRequest):
    return ingestion_service.ingest(
        source=request.source,
        loader_name=request.loader,
        chunker_name=request.chunker,
    )