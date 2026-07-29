from ..retrievers.base import BaseRetriever
from ..prompts.prompt_builder import PromptBuilder
from ..llms.base import BaseLLM

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

    def invoke(self, query: str, k: int = 5) -> str:
        documents = self.retriever.retrieve(query, k)
        prompt = self.prompt_builder.build_prompt(documents, query)
        return self.llm.generate(prompt)