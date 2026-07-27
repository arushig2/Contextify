from .base import BaseEmbedding
from ..core.config import settings 
from huggingface_hub import InferenceClient
from langchain_core.documents import Document


class BGEM3Embedding(BaseEmbedding):

    def __init__(self):
        self._client = InferenceClient(
            provider="hf-inference",
            api_key=settings.hf_api_key,
        )

        self._model = "BAAI/bge-m3"


    def _embed(self, text: str | list[str]) -> list[float] | list[list[float]]:
        try:
            embeddings = self._client.feature_extraction(
                text,
                model=self._model,
            )

            return embeddings.tolist()
        except Exception as e:
            raise RuntimeError("Failed to generate embeddings.") from e
         

    def embed_documents(self, documents: list[Document]) -> list[list[float]]:
        texts = [doc.page_content for doc in documents]
        return self._embed(texts)
       

                

    def embed_query(self, query: str) -> list[float]:
        return self._embed(query)
        