from .base import BaseRetriever
from langchain_core.documents import Document
from ..embeddings.base import BaseEmbedding
from ..vectordb.base import BaseVectorDB


class SimilarityRetriever(BaseRetriever):
    def __init__(self, embedding: BaseEmbedding, vector_db: BaseVectorDB):
        self.embedding = embedding
        self.vector_db = vector_db

    def retrieve(self, query: str, k: int = 5) -> list[Document]:
        query_vector = self.embedding.embed_query(query)
        results = self.vector_db.search(query_vector, k = k)
        return [result.document for result in results]