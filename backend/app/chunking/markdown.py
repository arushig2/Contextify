from .base import BaseChunker
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter


class MarkdownChunker(BaseChunker):

    def __init__(self, headers_to_split_on: list[tuple[str, str]] | None = None):
        if headers_to_split_on is None:
            headers_to_split_on = [
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ]
        self.splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)


    def split(self, documents: list[Document]) -> list[Document]:
        
        final_chunks = []

        for doc in documents:
            chunks = self.splitter.split_text(doc.page_content)

            # preserve original metadata
            for chunk in chunks:
                chunk.metadata.update(doc.metadata)

            final_chunks.extend(chunks)

        return final_chunks
