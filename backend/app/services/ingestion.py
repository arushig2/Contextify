import logging
from app.loaders.factory import LoaderFactory
from app.chunking.factory import ChunkerFactory
from app.embeddings.base import BaseEmbedding
from app.vectordb.base import BaseVectorDB

logger = logging.getLogger(__name__)

class IngestionService:

    def __init__(
        self,
        embedding: BaseEmbedding,
        vector_db: BaseVectorDB,
    ):
        self.embedding = embedding
        self.vector_db = vector_db
    

    def ingest(
        self,
        source: str,
        loader_name: str,
        chunker_name: str,
    ) -> dict:

        logger.info(f"Starting ingestion | source={source} | loader={loader_name}")

        # 1. Load documents
        loader = LoaderFactory.create(
            loader_name,
            source,
        )

        
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} document(s)")
        # 2. Split documents into chunks
        chunker = ChunkerFactory.create(chunker_name)

        
        logger.info("Chunking documents...")
        chunks = chunker.split(documents)
        logger.info(f"Generated {len(chunks)} chunks")

        # 3. Generate embeddings
        logger.info("Generating embeddings...")
        vectors = self.embedding.embed_documents(chunks)
        logger.info(f"Generated {len(vectors)} embeddings")

        self.vector_db.create_collection(vector_size=len(vectors[0]))

        # 4. Store chunks + vectors in Qdrant
        logger.info("Uploading vectors to Qdrant...")
        self.vector_db.add_documents(
            documents=chunks,
            embeddings=vectors
        )

        logger.info(
            f"Ingestion completed | documents={len(documents)} | chunks={len(chunks)}"
        )

        return {
            "message": "Documents ingested successfully",
            "documents": len(documents),
            "chunks": len(chunks),
        }