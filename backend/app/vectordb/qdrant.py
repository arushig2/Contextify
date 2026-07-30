import uuid
import logging
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.models import (Distance, VectorParams, PointStruct, Filter, FieldCondition, 
                                  MatchAny, PayloadSchemaType)
from ..core.config import settings
from .base import BaseVectorDB
from ..models.vector_search_result import VectorSearchResult

logger = logging.getLogger(__name__)

class QdrantVectorDB(BaseVectorDB):
      
    def __init__(self, collection_name: str):
        self._client = QdrantClient(
            url = settings.qdrant_url,
            api_key = settings.qdrant_api_key,
            timeout=60
        )

        self._collection_name = collection_name
        

    def create_collection(self, vector_size: int) -> None:
        try:
            if not self._client.collection_exists(self._collection_name):
                self._client.create_collection(
                    collection_name=self._collection_name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE,
                    ),
                )

            # Ensure payload indexes exist
            self._client.create_payload_index(
                collection_name=self._collection_name,
                field_name="source",
                field_schema=PayloadSchemaType.KEYWORD,
            )

        except Exception as e:
            raise RuntimeError(
                "Error occurred while creating the collection."
            ) from e

    def add_documents(self, documents: list[Document], embeddings: list[list[float]]) -> None:

        points: list[PointStruct] = []
        if len(documents) != len(embeddings):
            raise ValueError("The number of documents must match the number of embeddings.")

        sources = list({
            document.metadata["source"]
            for document in documents
            if "source" in document.metadata
        })

        if not sources:
            raise ValueError("Documents must contain a 'source' in metadata.")
        
        for (document, embedding) in zip(documents, embeddings):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        **document.metadata,
                        "text": document.page_content                        
                    },
                )
            )

        try:
            logger.info(f"Deleting existing documents for source(s): {sources}")

            self._client.delete(
                collection_name=self._collection_name,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="source",
                            match=MatchAny(any=sources),
                        )
                    ]
                ),
                wait=True,
            )

            points: list[PointStruct] = []

            for document, embedding in zip(documents, embeddings):
                points.append(
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding,
                        payload={
                            **document.metadata,
                            "text": document.page_content,
                        },
                    )
                )

            self._client.upsert(
                collection_name=self._collection_name,
                points=points,
            )

            logger.info(f"Successfully indexed {len(points)} points for source(s): {sources}")

        except Exception as e:
            logger.exception("Failed to replace documents in Qdrant.")

            raise RuntimeError("Error occurred while replacing documents.") from e
        

    def search(self, query_embedding: list[float], k: int = 5) -> list[VectorSearchResult]:
        try:
            results = self._client.query_points(
                collection_name=self._collection_name,
                query=query_embedding,
                limit=k,
                with_vectors=True
            )

            search_results: list[VectorSearchResult] = []

            for point in results.points:

                payload = point.payload

                document = Document(
                    page_content=payload["text"],
                    metadata={
                        key: value
                        for key, value in payload.items()
                        if key != "text"
                    }
                )

                search_results.append(
                    VectorSearchResult(
                        document=document,
                        score=point.score,
                        embedding=point.vector,
                    )
                )

            return search_results

        except Exception as e:
            raise RuntimeError("Error occurred while searching the collection.") from e

    def delete_collection(self) -> None:
        try:
            if self._client.collection_exists(self._collection_name):
                self._client.delete_collection(self._collection_name)
        except Exception as e:
            raise RuntimeError("Error occurred while deleting the collection.") from e



    
    