import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompt_values import ChatPromptValue
from ..core.config import settings
from .base import BaseLLM

logger = logging.getLogger(__name__)

class GeminiLLM(BaseLLM):

    def __init__(self):
        self._llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=0.0)

    def generate(self, prompt:ChatPromptValue):
        logger.info("Sending prompt to Gemini")
        response = self._llm.invoke(prompt)
        logger.info("Gemini response received")
        return response.content