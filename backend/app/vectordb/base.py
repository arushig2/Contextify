from abc import ABC, abstractmethod
from langchain_core.documents import Document


class BaseVectorDB(ABC):

    @abstractmethod
    def create_collection(self, vector_size: int) -> None:
        pass

    @abstractmethod
    def add_documents(self, documents: list[Document], embeddings: list[list[float]]) -> None:
        pass

    @abstractmethod
    def search(self, query_embedding: list[float], k: int = 5) -> list[Document]:
        pass

    @abstractmethod
    def delete_collection(self) -> None:
        pass