from time import perf_counter
import logging
from langchain_core.documents import Document
from .base import BaseRetriever
from ..embeddings.base import BaseEmbedding
from ..vectordb.base import BaseVectorDB

logger = logging.getLogger(__name__)

class SimilarityRetriever(BaseRetriever):
    def __init__(self, embedding: BaseEmbedding, vector_db: BaseVectorDB):
        self.embedding = embedding
        self.vector_db = vector_db

    def retrieve(self, query: str, k: int = 5) -> list[Document]:

        embed_start = perf_counter()
        query_vector = self.embedding.embed_query(query)
        embedding_ms = (perf_counter() - embed_start) * 1000

        search_start = perf_counter()
        results = self.vector_db.search(query_vector, k=k)
        search_ms = (perf_counter() - search_start) * 1000

        logger.info(
            f"Retriever completed | "
            f"embedding={embedding_ms:.2f}ms | "
            f"search={search_ms:.2f}ms"
        )

        return [result.document for result in results]