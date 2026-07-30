from app.retrievers.base import BaseRetriever
from app.prompts.prompt_builder import PromptBuilder
from app.llms.base import BaseLLM

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
        documents = self.retriever.retrieve(query, k)
        prompt = self.prompt_builder.build_prompt(documents, query)
        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "documents": documents,
        }