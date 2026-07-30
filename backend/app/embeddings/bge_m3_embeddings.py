import time
import logging
from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError
from langchain_core.documents import Document
from .base import BaseEmbedding
from ..core.config import settings 

logger = logging.getLogger(__name__)

class BGEM3Embedding(BaseEmbedding):

    def __init__(self):
        self._client = InferenceClient(
            provider="hf-inference",
            api_key=settings.hf_api_key,
        )

        self._model = "BAAI/bge-m3"
        self.BATCH_SIZE = settings.embedding_batch_size
        self.MAX_RETRIES = settings.embedding_max_retries

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:

        for attempt in range(1, self.MAX_RETRIES + 1):

            try:
                embeddings = self._client.feature_extraction(
                    texts,
                    model=self._model,
                )

                return embeddings.tolist()

            except HfHubHTTPError as e:

                logger.warning(
                    "Embedding batch failed (attempt %d/%d): %s",
                    attempt,
                    self.MAX_RETRIES,
                    e,
                )

                if attempt == self.MAX_RETRIES:
                    raise RuntimeError(
                        "Failed to generate embeddings."
                    ) from e

                time.sleep(2 ** attempt)


    def embed_documents(
        self,
        documents: list[Document],
    ) -> list[list[float]]:

        texts = [doc.page_content for doc in documents]

        logger.info(
            "Generating embeddings for %d chunks",
            len(texts),
        )

        embeddings = []

        total_batches = (
            len(texts) + self.BATCH_SIZE - 1
        ) // self.BATCH_SIZE

        for i in range(0, len(texts), self.BATCH_SIZE):

            batch = texts[i:i + self.BATCH_SIZE]

            logger.info(
                "Embedding batch %d/%d",
                i // self.BATCH_SIZE + 1,
                total_batches,
            )

            embeddings.extend(
                self._embed_batch(batch)
            )

        logger.info(
            "Generated %d embeddings",
            len(embeddings),
        )

        return embeddings
       

    def embed_query(self, query: str) -> list[float]:

        embedding = self._client.feature_extraction(
            query,
            model=self._model,
        )

        return embedding.tolist()