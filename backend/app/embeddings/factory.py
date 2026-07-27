from .base import BaseEmbedding
from .bge_m3_embeddings import BGEM3Embedding


class EmbeddingFactory:
    _registry = {
        "bge-m3": BGEM3Embedding,
    }

    @staticmethod
    def create(model: str, **kwargs) -> BaseEmbedding:
        try:
            embedding_cls = EmbeddingFactory._registry[model]
        except KeyError:
            raise ValueError(f"Unknown embedding model: {model}")

        return embedding_cls(**kwargs)