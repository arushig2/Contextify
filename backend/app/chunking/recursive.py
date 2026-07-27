from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .base import BaseChunker


class RecursiveChunker(BaseChunker):

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, separators: list[str] | None = None):
        if separators is None:
            separators = ["\n\n", "\n", " ", ""]

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            separators=separators)

    def split(self, documents: list[Document]) -> list[Document]:
        return self.splitter.split_documents(documents)
