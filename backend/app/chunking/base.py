from abc import ABC, abstractmethod
from langchain_core.documents import Document


class BaseChunker(ABC):
     
    @abstractmethod
    def split(self, documents: list[Document]) -> list[Document]:
    
        raise NotImplementedError
