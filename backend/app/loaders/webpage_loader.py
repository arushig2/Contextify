import logging
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from .base import BaseLoader

logger = logging.getLogger(__name__)

class WebPageLoader(BaseLoader):
    def __init__(self, source: str) -> None:
        super().__init__(
            source=source,
            source_type="url",
        )

    def load(self) -> list[Document]:
        loader = WebBaseLoader(self.source)
        documents = loader.load()

        for document in documents:
            document.metadata["source"] = self.source
            document.metadata["source_type"] = "web"

        return documents