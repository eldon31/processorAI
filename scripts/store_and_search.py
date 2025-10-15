import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from pydantic import BaseModel, Field, ValidationError, field_validator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from qdrant_client import QdrantClient
    from qdrant_client.models import PointStruct
    from sentence_transformers import SentenceTransformer


class EmbeddedChunk(BaseModel):
    index: int
    text: str
    char_count: int = 0
    token_count: int = 0
    meta: Dict[str, Any] = Field(default_factory=dict)
    embedding: List[float]
    embedding_model: str
    embedding_dimension: int

    @field_validator("embedding")
    def embedding_not_empty(cls, value: List[float]) -> List[float]:
        if not value:
            raise ValueError("Embedding vector is empty")
        return value

    def to_qdrant_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "text": self.text,
            "char_count": self.char_count,
            "token_count": self.token_count,
            "embedding_model": self.embedding_model,
            "embedding_dimension": self.embedding_dimension,
        }

        meta_source = self.meta.get("source")
        if meta_source:
            payload["source"] = meta_source

        headings = self.meta.get("headings")
        if isinstance(headings, list):
            payload["headings"] = headings

        return payload


class SearchResult(BaseModel):
    id: Any
    score: float
    text: str
    char_count: int
    token_count: int
    source: Optional[str] = None
    headings: List[str] = Field(default_factory=list)


class QdrantStore:
    def __init__(
        self,
        collection_name: str = "inngest_docs",
        vector_size: int = 384,
        host: str = "localhost",
        port: int = 6333,
        use_memory: bool = True,
    ):
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.host = host
        self.port = port
        self.use_memory = use_memory
        self.client = self._connect()

    def _connect(self) -> "QdrantClient":
        try:
            from qdrant_client import QdrantClient

            if self.use_memory:
                client = QdrantClient(":memory:")
                logger.info("Connected to in-memory Qdrant")
            else:
                client = QdrantClient(host=self.host, port=self.port)
                logger.info(f"Connected to Qdrant at {self.host}:{self.port}")
            return client
        except Exception as exc:
            logger.error(f"Failed to connect to Qdrant: {exc}")
            raise

    def create_collection(self) -> None:
        try:
            from qdrant_client.models import Distance, VectorParams

            collections = self.client.get_collections()
            existing = {collection.name for collection in collections.collections}

            if self.collection_name in existing:
                logger.info(f"Collection '{self.collection_name}' already exists; deleting for clean state")
                try:
                    self.client.delete_collection(self.collection_name)
                except Exception as exc:
                    logger.warning(f"Could not delete existing collection: {exc}")

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )
            logger.info(f"Created collection '{self.collection_name}' with vector size {self.vector_size}")
        except Exception as exc:
            logger.error(f"Failed to create collection: {exc}")
            raise

    def add_embeddings(self, chunks: List[EmbeddedChunk]) -> int:
        try:
            from qdrant_client.models import PointStruct

            points: List[PointStruct] = []
            for chunk in chunks:
                point = PointStruct(
                    id=chunk.index,
                    vector=chunk.embedding,
                    payload=chunk.to_qdrant_payload(),
                )
                points.append(point)

            if not points:
                logger.warning("No embeddings to add")
                return 0

            batch_size = 100
            for index in range(0, len(points), batch_size):
                batch = points[index : index + batch_size]
                self.client.upsert(collection_name=self.collection_name, points=batch)
                logger.info(f"Added batch of {len(batch)} points to Qdrant")

            logger.info(f"Successfully added {len(points)} embeddings to Qdrant")
            return len(points)
        except Exception as exc:
            logger.error(f"Failed to add embeddings to Qdrant: {exc}")
            raise

    def search(self, query_embedding: List[float], limit: int = 5) -> List[SearchResult]:
        try:
            raw_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
            )

            parsed_results: List[SearchResult] = []
            for hit in raw_results:
                payload = hit.payload or {}
                try:
                    parsed_results.append(
                        SearchResult(
                            id=hit.id,
                            score=hit.score,
                            text=payload.get("text", ""),
                            char_count=payload.get("char_count", 0),
                            token_count=payload.get("token_count", 0),
                            source=payload.get("source"),
                            headings=payload.get("headings", []),
                        )
                    )
                except ValidationError as err:
                    logger.warning(f"Skipping invalid search result: {err}")
            return parsed_results
        except Exception as exc:
            logger.error(f"Failed to search Qdrant: {exc}")
            raise

    def get_collection_info(self) -> Optional[Dict[str, Any]]:
        try:
            info = self.client.get_collection(self.collection_name)
            config = getattr(info, "config", None)
            params = getattr(config, "params", None)
            vectors = getattr(params, "vectors", None)

            vector_size = None
            distance = None
            if isinstance(vectors, dict):
                vector_size = vectors.get("size")
                distance = vectors.get("distance")
            else:
                vector_size = getattr(vectors, "size", None)
                distance = getattr(vectors, "distance", None)

            return {
                "name": self.collection_name,
                "vector_size": vector_size,
                "distance": distance,
                "points_count": getattr(info, "points_count", None),
            }
        except Exception as exc:
            logger.error(f"Failed to get collection info: {exc}")
            return None


class RAGPipeline:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model: Optional["SentenceTransformer"] = None
        self._qdrant: Optional[QdrantStore] = None
        self._load_model()

    @property
    def model(self) -> "SentenceTransformer":
        if self._model is None:
            raise RuntimeError("Embedding model not loaded")
        return self._model

    @property
    def qdrant(self) -> QdrantStore:
        if self._qdrant is None:
            raise RuntimeError("Qdrant not initialized")
        return self._qdrant

    def _load_model(self) -> None:
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name, device="cpu")
            logger.info("Embedding model loaded successfully")
        except Exception as exc:
            logger.error(f"Failed to load embedding model: {exc}")
            raise

    def embed_query(self, query: str) -> List[float]:
        try:
            return self.model.encode(query, convert_to_numpy=True).tolist()
        except Exception as exc:
            logger.error(f"Failed to embed query: {exc}")
            raise

    def initialize_qdrant(self, collection_name: str = "inngest_docs", vector_size: int = 384) -> None:
        try:
            self._qdrant = QdrantStore(collection_name=collection_name, vector_size=vector_size)
            self.qdrant.create_collection()
            logger.info("Qdrant initialized successfully")
        except Exception as exc:
            logger.error(f"Failed to initialize Qdrant: {exc}")
            raise

    def search(self, query: str, limit: int = 5) -> List[SearchResult]:
        if self._qdrant is None:
            raise RuntimeError("Qdrant not initialized. Call initialize_qdrant() first.")
        query_embedding = self.embed_query(query)
        return self.qdrant.search(query_embedding, limit=limit)


def load_embedded_chunks(file_path: str) -> List[EmbeddedChunk]:
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        raw_chunks = data.get("embedded_chunks", [])
        validated: List[EmbeddedChunk] = []

        for raw_chunk in raw_chunks:
            try:
                validated.append(EmbeddedChunk(**raw_chunk))
            except ValidationError as err:
                logger.warning(f"Skipping invalid chunk: {err}")

        logger.info(f"Loaded {len(validated)} embedded chunks from {file_path}")
        return validated
    except Exception as exc:
        logger.error(f"Failed to load embedded chunks from {file_path}: {exc}")
        return []


def main() -> None:
    embedded_chunks_file = Path("output/chunks/embedded_chunks.json")
    collection_name = "inngest_docs"
    model_name = "all-MiniLM-L6-v2"
    vector_size = 384

    logger.info("Starting RAG pipeline: Store and Search")
    logger.info(f"Embedded chunks file: {embedded_chunks_file}")
    logger.info(f"Collection: {collection_name}")
    logger.info(f"Model: {model_name}")

    chunks = load_embedded_chunks(str(embedded_chunks_file))
    if not chunks:
        logger.error("No embedded chunks loaded, exiting")
        sys.exit(1)

    try:
        rag = RAGPipeline(model_name=model_name)
        rag.initialize_qdrant(collection_name=collection_name, vector_size=vector_size)
    except Exception:
        logger.error("Failed to initialize RAG pipeline")
        sys.exit(1)

    try:
        stored = rag.qdrant.add_embeddings(chunks)
        logger.info(f"Successfully stored {stored} embeddings in Qdrant")
    except Exception:
        logger.error("Failed to store embeddings")
        sys.exit(1)

    test_queries = [
        "What are Inngest apps?",
        "How do apps work in Inngest?",
        "Tell me about app deployment",
    ]

    logger.info("\n" + "=" * 50)
    logger.info("TESTING SEARCH FUNCTIONALITY")
    logger.info("=" * 50)

    for query in test_queries:
        logger.info(f"\nQuery: '{query}'")
        try:
            results = rag.search(query, limit=3)
            if not results:
                logger.info("  No results found")
            for position, result in enumerate(results, 1):
                logger.info(f"Result {position} (Score: {result.score:.3f}):")
                logger.info(f"  Text: {result.text[:100]}...")
                if result.headings:
                    logger.info(f"  Headings: {result.headings}")
                logger.info(f"  Source: {result.source or 'N/A'}")
        except Exception as exc:
            logger.error(f"Search failed for query '{query}': {exc}")

    try:
        info = rag.qdrant.get_collection_info()
        if info:
            logger.info("Collection Info:")
            logger.info(f"  Name: {info['name']}")
            logger.info(f"  Vector Size: {info['vector_size']}")
            logger.info(f"  Distance: {info['distance']}")
            logger.info(f"  Points Count: {info['points_count']}")
    except Exception as exc:
        logger.error(f"Failed to get collection info: {exc}")

    logger.info("\nRAG pipeline completed successfully!")


if __name__ == "__main__":
    main()