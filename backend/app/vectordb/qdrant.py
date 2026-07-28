import uuid
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from ..core.config import settings
from .base import BaseVectorDB


class QdrantVectorDB(BaseVectorDB):
      
    def __init__(self, collection_name: str):
        self._client = QdrantClient(
            url = settings.qdrant_url,
            api_key = settings.qdrant_api_key
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
        except Exception as e:
            raise RuntimeError("Error occurred while creating the collection.") from e

    def add_documents(self, documents: list[Document], embeddings: list[list[float]]) -> None:

        points: list[PointStruct] = []
        if len(documents) != len(embeddings):
            raise ValueError("The number of documents must match the number of embeddings.")
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
            self._client.upsert(
                collection_name=self._collection_name,
                points=points,
            )
        except Exception as e:
            raise RuntimeError("Error occurred while adding documents.") from e
        

    def search(self, query_embedding: list[float], k: int = 5) -> list[Document]:
        try:
            results = self._client.query_points(
                collection_name=self._collection_name,
                query=query_embedding,
                limit=k,
            )

            documents: list[Document] = []

            for point in results.points:
                payload = point.payload

                documents.append(
                    Document(
                        page_content=payload["text"],
                        metadata={
                                **{key: value
                                for key, value in payload.items()
                                if key != "text"
                            },
                            "_score":point.score
                        }
                    )
                )

            return documents

        except Exception as e:
            raise RuntimeError("Error occurred while searching the collection.") from e

    def delete_collection(self) -> None:
        try:
            if self._client.collection_exists(self._collection_name):
                self._client.delete_collection(self._collection_name)
        except Exception as e:
            raise RuntimeError("Error occurred while deleting the collection.") from e



    
    