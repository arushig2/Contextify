from fastapi import FastAPI
import uvicorn
from .api.router import router 
import logging
import app.core.logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Contextify",
    version="1.0.0",
)

app.include_router(router)


if __name__ == "__main__":

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )