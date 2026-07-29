from langchain_core.documents import Document
from .rag_prompt import RAG_PROMPT

class PromptBuilder:

    def build_context(self, documents: list[Document]) -> str:
        """Combine retrieved documents into a single context string."""
        if not documents:
            return ""
        sections = []

        for i, document in enumerate(documents, start=1):
            source = document.metadata.get("source", "Unknown")

            sections.append(
                f"Document {i}\n"
                f"Source: {source}\n\n"
                f"{document.page_content}"
            )

        return "\n\n---\n\n".join(sections)

    def build_prompt(self, documents: list[Document], question: str):
        """Formats retrieved documents into a prompt for the LLM."""
        context = self.build_context(documents)

        return RAG_PROMPT.invoke({
            "context": context,
            "question": question
        })