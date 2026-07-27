from abc import ABC, abstractmethod
from typing import Literal

from langchain_core.documents import Document


SourceType = Literal["url", "text"]


class BaseLoader(ABC):
    """
    Base contract for all document loaders.

    Each loader accepts a source and must implement
    a method that returns LangChain Document objects.
    """

    def __init__(
        self,
        source: str,
        source_type: SourceType,
    ) -> None:
        self.source = source
        self.source_type = source_type

    @abstractmethod
    def load(self) -> list[Document]:
        """
        Load the source and return LangChain Documents.

        Every concrete loader must implement this method.
        """
        raise NotImplementedError

    def get_content(self) -> str:
        """
        Return the combined text content of all loaded documents.
        """
        documents = self.load()

        return "\n\n".join(
            document.page_content
            for document in documents
        )