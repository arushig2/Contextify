import numpy as np
from .base import BaseRetriever
from langchain_core.documents import Document
from ..embeddings.base import BaseEmbedding
from ..vectordb.base import BaseVectorDB
from ..models.vector_search_result import VectorSearchResult


class MMRRetriever(BaseRetriever):
    def __init__(self, embedding: BaseEmbedding,
                 vector_db: BaseVectorDB, 
                 fetch_k : int = 20, 
                 lambda_mult: float = 0.5,):
        
        self.embedding = embedding
        self.vector_db = vector_db
        if not 0 <= lambda_mult <= 1:
            raise ValueError(
                "lambda_mult must be between 0 and 1."
            )
        if fetch_k <= 0:
            raise ValueError(
                "fetch_k must be greater than 0."
            )
        self.fetch_k = fetch_k
        self.lambda_mult = lambda_mult

    def _normalize(self, vector: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(vector)
        return vector if norm == 0 else vector / norm

    def _select_documents(self, query_vector: list[float], candidates : list[VectorSearchResult], k:int)->list[VectorSearchResult]:
        if not candidates or k <= 0:
            return []

        k = min(k, len(candidates))

        query_vector = self._normalize(np.array(query_vector))

        candidate_vectors = np.array([
            self._normalize(np.array(candidate.embedding))
            for candidate in candidates
        ])

        query_similarities = np.array([
            np.dot(query_vector, vector)
            for vector in candidate_vectors
        ])

        selected_indices = []
        remaining_indices = list(range(len(candidates)))

        for _ in range(k):
            if not selected_indices:
                best_idx = remaining_indices[
                    np.argmax(query_similarities[remaining_indices])
                ]

            else:
                mmr_scores = []

                for idx in remaining_indices:

                    relevance = query_similarities[idx]

                    diversity = max(
                        np.dot(
                            candidate_vectors[idx],
                            candidate_vectors[selected_idx]
                        )
                        for selected_idx in selected_indices
                    )

                    mmr_score = (
                        self.lambda_mult * relevance
                        - (1 - self.lambda_mult) * diversity
                    )

                    mmr_scores.append((idx, mmr_score))

                best_idx = max(
                    mmr_scores,
                    key=lambda x: x[1]
                )[0]

            selected_indices.append(best_idx)
            remaining_indices.remove(best_idx)

        return [
            candidates[idx]
            for idx in selected_indices
        ]

    def retrieve(self, query: str, k: int = 5) -> list[Document]:
        query_vector = self.embedding.embed_query(query)
        candidates = self.vector_db.search(query_vector, k=max(self.fetch_k, k))
        selected = self._select_documents(query_vector, candidates, k)
        return [result.document for result in selected]
        

