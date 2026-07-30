from app.loaders.factory import LoaderFactory
from app.chunking.factory import ChunkerFactory
from app.embeddings.base import BaseEmbedding
from app.vectordb.base import BaseVectorDB


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

        # 1. Load documents
        loader = LoaderFactory.create(
            loader_name,
            source,
        )

        documents = loader.load()

        # 2. Split documents into chunks
        chunker = ChunkerFactory.create(chunker_name)

        chunks = chunker.split(documents)

        # 3. Generate embeddings
        vectors = self.embedding.embed_documents(chunks)

        self.vector_db.create_collection(vector_size=len(vectors[0]))

        # 4. Store chunks + vectors in Qdrant
        self.vector_db.add_documents(
            documents=chunks,
            embeddings=vectors
        )

        return {
            "message": "Documents ingested successfully",
            "documents": len(documents),
            "chunks": len(chunks),
        }