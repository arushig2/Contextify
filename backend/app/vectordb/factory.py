from .base import BaseVectorDB
from .qdrant import QdrantVectorDB


class VectorDBFactory:
    _registry = {
        "qdrant": QdrantVectorDB,
    }

    @staticmethod
    def create(db_name: str, **kwargs) -> BaseVectorDB:
        try:
            vector_db_cls = VectorDBFactory._registry[db_name]
        except KeyError:
            raise ValueError(f"Unknown vector db: {db_name}")

        return vector_db_cls(**kwargs)