from abc import ABC, abstractmethod
from langchain_core.documents import Document


class BaseEmbedding(ABC):

    @abstractmethod
    def embed_documents(
        self,
        documents: list[Document]
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple documents.
        """
        pass

    @abstractmethod
    def embed_query(
        self,
        query: str
    ) -> list[float]:
        """
        Generate embedding for a single user query.
        """
        pass