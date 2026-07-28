from .base import BaseRetriever
from .mmr import MMRRetriever
from .similarity import SimilarityRetriever


class RetrieverFactory:
    _registry = {
        "mmr": MMRRetriever,
        "similarity": SimilarityRetriever
    }

    @staticmethod
    def create(strategy: str, **kwargs) -> BaseRetriever:
        try:
            retriever_cls = RetrieverFactory._registry[strategy]
        except KeyError:
            raise ValueError(f"Unknown retrival strategy: {strategy}")

        return retriever_cls(**kwargs)