from .embeddings.factory import EmbeddingFactory
from .vectordb.factory import VectorDBFactory
from .retrievers.factory import RetrieverFactory
from .prompts.prompt_builder import PromptBuilder
from .llms.gemini import GeminiLLM
from .chains.rag_chain import RAGChain
from .services.ingestion import IngestionService
from .core.config import settings

embedding = EmbeddingFactory.create("bge-m3")

vector_db = VectorDBFactory.create("qdrant", collection_name = settings.qdrant_collection)

retriever = RetrieverFactory.create("similarity", embedding = embedding, vector_db = vector_db)

prompt_builder = PromptBuilder()

llm = GeminiLLM()

rag_chain = RAGChain(
    retriever,
    prompt_builder,
    llm,
)

ingestion_service = IngestionService(
    embedding=embedding,
    vector_db=vector_db,
)