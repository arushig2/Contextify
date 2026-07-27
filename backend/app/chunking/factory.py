from .base import BaseChunker
from .recursive import RecursiveChunker
from .markdown import MarkdownChunker

class ChunkerFactory:
    _registry = {
        "recursive": RecursiveChunker,
        "markdown": MarkdownChunker,
    }

    @staticmethod
    def create(strategy: str, **kwargs) -> BaseChunker:
        try:
            chunker_cls = ChunkerFactory._registry[strategy]
        except KeyError:
            raise ValueError(f"Unknown chunking strategy: {strategy}")

        return chunker_cls(**kwargs)