from time import perf_counter
import logging
from app.retrievers.base import BaseRetriever
from app.prompts.prompt_builder import PromptBuilder
from app.llms.base import BaseLLM

logger = logging.getLogger(__name__)

class RAGChain:

    def __init__(
        self,
        retriever: BaseRetriever,
        prompt_builder: PromptBuilder,
        llm:BaseLLM
    ):

        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm = llm

    def invoke(self, query: str, k: int = 5) -> dict:
        logger.info("Received new query")
        total_start = perf_counter()

        documents = self.retriever.retrieve(query, k)

        prompt = self.prompt_builder.build_prompt(documents, query)

        generation_start = perf_counter()
        answer = self.llm.generate(prompt)
        generation_ms = (perf_counter() - generation_start) * 1000

        total_ms = (perf_counter() - total_start) * 1000

        logger.info(
            "Query completed | "
            f"chunks={len(documents)} | "
            f"generation={generation_ms:.2f}ms | "
            f"total={total_ms:.2f}ms"
        )

        return {
            "answer": answer,
            "documents": documents,
            "metrics": {
                "generation_ms": round(generation_ms, 2),
                "total_ms": round(total_ms, 2),
            },
        }