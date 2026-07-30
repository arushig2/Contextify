from fastapi import APIRouter

from .routes.health import router as health_router
from .routes.query import router as query_router
from .routes.ingest import router as ingestion_router


router = APIRouter()

router.include_router(health_router)
router.include_router(query_router)
router.include_router(ingestion_router)