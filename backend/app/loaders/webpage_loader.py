import logging
from .base import BaseLoader
from langchain_community.document_loaders import WebBaseLoader

logger = logging.getLogger(__name__)

class WebPageLoader(BaseLoader):
    def __init__(self, source: str) -> None:
        super().__init__(
            source=source,
            source_type="url",
        )

    def load(self):
        loader = WebBaseLoader(self.source)
        return loader.load()
