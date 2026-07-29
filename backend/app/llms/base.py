from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """Abstract base class for all LLM providers."""

    @abstractmethod
    def generate(self, prompt):
        """Generate a response from the given prompt."""
        pass