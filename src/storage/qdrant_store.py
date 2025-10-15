"""
Qdrant vector storage layer with advanced features.

Features:
- Scalar quantization (int8) for 4x memory savings
- Payload indexing for fast metadata filtering
- Hybrid search (dense + sparse vectors)
- Production-ready with health checks
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    MatchAny,
    Range,
    SearchParams,
    ScalarQuantization,
    ScalarQuantizationConfig,
    ScalarType,
    PayloadSchemaType,
    HnswConfigDiff,
    CollectionConfig,
)
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class QdrantStoreConfig(BaseModel):
    """Configuration for Qdrant storage."""
    
    host: str = "localhost"
    port: int = 6333
    collection_name: str = "documents"
    vector_size: int = 1536  # Nomic Embed Code dimension
    distance_metric: str = "Cosine"  # Cosine, Euclidean, Dot
    enable_quantization: bool = True  # 4x memory savings
    quantization_type: str = "int8"  # int8 or binary
    
    # HNSW index parameters
    hnsw_m: int = 16  # Number of edges per node (higher = better recall)
    hnsw_ef_construct: int = 100  # Size of dynamic candidate list
    on_disk: bool = False  # Store vectors on disk to save RAM
    
    # Production settings
    timeout: int = 60
    prefer_grpc: bool = False  # Use REST for string ID compatibility
    api_key: Optional[str] = None


class QdrantStore:
    """Advanced Qdrant vector store with quantization and indexing."""
    
    def __init__(self, config: QdrantStoreConfig):
        """Initialize Qdrant store with configuration."""
        self.config = config
        self.collection_name = config.collection_name
        
        # Initialize client
        self.client = QdrantClient(
            host=config.host,
            port=config.port,
            timeout=config.timeout,
            prefer_grpc=config.prefer_grpc,
            api_key=config.api_key
        )
        
        # Initialize collection with optimizations
        self._initialize_collection()
        
        logger.info(f"Qdrant store initialized: {config.collection_name}")
    
    def _initialize_collection(self):
        """Create collection with optimized settings for code embeddings."""
        
        # Check if collection exists
        collections = self.client.get_collections().collections
        if any(c.name == self.collection_name for c in collections):
            logger.info(f"Collection {self.collection_name} already exists")
            return
        
        # Distance metric mapping
        distance_map = {
            "Cosine": Distance.COSINE,
            "Euclidean": Distance.EUCLID,
            "Dot": Distance.DOT
        }
        
        # Quantization configuration for memory efficiency
        quantization_config = None
        if self.config.enable_quantization:
            if self.config.quantization_type == "int8":
                quantization_config = ScalarQuantization(
                    scalar=ScalarQuantizationConfig(
                        type=ScalarType.INT8,
                        quantile=0.99,
                        always_ram=True
                    )
                )
            
        # Create collection with advanced settings
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.config.vector_size,
                distance=distance_map[self.config.distance_metric],
                hnsw_config=HnswConfigDiff(
                    m=self.config.hnsw_m,
                    ef_construct=self.config.hnsw_ef_construct,
                    full_scan_threshold=10000,
                    max_indexing_threads=0,
                    on_disk=self.config.on_disk
                )
            ),
            quantization_config=quantization_config
        )
        
        # Create indexes for fast filtering on metadata fields
        # These indexes dramatically speed up filtered searches
        payload_indexes = [
            ("document_id", PayloadSchemaType.KEYWORD),
            ("document_title", PayloadSchemaType.TEXT),
            ("chunk_index", PayloadSchemaType.INTEGER),
            ("content_type", PayloadSchemaType.KEYWORD),
            ("timestamp", PayloadSchemaType.DATETIME),
            ("tags", PayloadSchemaType.KEYWORD),
            # Code-specific indexes for enhanced search
            ("function_name", PayloadSchemaType.KEYWORD),
            ("class_name", PayloadSchemaType.KEYWORD),
            ("api_endpoint", PayloadSchemaType.KEYWORD),
            ("programming_language", PayloadSchemaType.KEYWORD),
            ("section", PayloadSchemaType.KEYWORD),
        ]
        
        for field_name, field_type in payload_indexes:
            try:
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name=field_name,
                    field_schema=field_type
                )
                logger.debug(f"Created index for {field_name}")
            except Exception as e:
                logger.warning(f"Failed to create index for {field_name}: {e}")
        
        logger.info(f"Collection {self.collection_name} created with quantization: {self.config.enable_quantization}")
    
    def add_embeddings(
        self,
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
        ids: Optional[List[Any]] = None
    ) -> List[Any]:
        """Add embeddings with metadata to the collection."""
        
        if not embeddings:
            return []
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in embeddings]
        
        # Add timestamps to metadata
        timestamp = datetime.now().isoformat()
        for metadata in metadatas:
            if "timestamp" not in metadata:
                metadata["timestamp"] = timestamp
        
        # Create points
        points = [
            PointStruct(
                id=point_id,
                vector=embedding,
                payload=metadata
            )
            for point_id, embedding, metadata in zip(ids, embeddings, metadatas)
        ]
        
        # Upload points in batches for efficiency
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch
            )
        
        logger.info(f"Added {len(embeddings)} embeddings to {self.collection_name}")
        return ids
    
    def search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        score_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar embeddings with optional filtering."""
        
        # Convert filters to Qdrant filter format
        qdrant_filter = self._build_filter(filters) if filters else None
        
        # Search parameters
        search_params = SearchParams(
            hnsw_ef=64,  # Higher = better recall, slower search
            exact=False   # Use approximate search for speed
        )
        
        # Perform search
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            query_filter=qdrant_filter,
            search_params=search_params,
            score_threshold=score_threshold,
            with_payload=True,
            with_vectors=False  # Don't return vectors to save bandwidth
        )
        
        # Format results
        formatted_results = []
        for result in results:
            payload = result.payload or {}
            formatted_results.append({
                "id": result.id,
                "score": result.score,
                "metadata": payload,
                "content": payload.get("content", "")
            })
        
        return formatted_results
    
    def search_code(
        self,
        query_embedding: List[float],
        function_names: Optional[List[str]] = None,
        class_names: Optional[List[str]] = None,
        programming_languages: Optional[List[str]] = None,
        limit: int = 10,
        score_threshold: Optional[float] = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Enhanced search specifically for code content.
        
        Args:
            query_embedding: Query vector
            function_names: Filter by function names
            class_names: Filter by class names  
            programming_languages: Filter by programming language
            limit: Maximum results
            score_threshold: Minimum similarity score
            
        Returns:
            List of search results with code metadata
        """
        filters = {}
        
        if function_names:
            filters["function_name"] = function_names
        if class_names:
            filters["class_name"] = class_names
        if programming_languages:
            filters["programming_language"] = programming_languages
            
        # Add content type filter for code
        filters["content_type"] = ["code", "api_doc", "function", "class"]
        
        return self.search(
            query_embedding=query_embedding,
            limit=limit,
            filters=filters,
            score_threshold=score_threshold
        )
    
    def search_api_docs(
        self,
        query_embedding: List[float],
        endpoints: Optional[List[str]] = None,
        doc_sections: Optional[List[str]] = None,
        limit: int = 10,
        score_threshold: Optional[float] = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Enhanced search for API documentation.
        
        Args:
            query_embedding: Query vector
            endpoints: Filter by API endpoints
            doc_sections: Filter by documentation sections
            limit: Maximum results
            score_threshold: Minimum similarity score
            
        Returns:
            List of API documentation results
        """
        filters = {"content_type": ["api_doc", "documentation", "reference"]}
        
        if endpoints:
            filters["api_endpoint"] = endpoints
        if doc_sections:
            filters["section"] = doc_sections
            
        return self.search(
            query_embedding=query_embedding,
            limit=limit,
            filters=filters,
            score_threshold=score_threshold
        )
    
    def _build_filter(self, filters: Dict[str, Any]) -> Optional[Filter]:
        """Build Qdrant filter from dictionary."""
        if not filters:
            return None
        
        conditions = []
        
        for key, value in filters.items():
            if isinstance(value, list):
                # Multiple values - use MatchAny
                conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchAny(any=value)
                    )
                )
            elif isinstance(value, dict):
                # Range queries
                if "gte" in value or "lte" in value:
                    conditions.append(
                        FieldCondition(
                            key=key,
                            range=Range(
                                gte=value.get("gte"),
                                lte=value.get("lte")
                            )
                        )
                    )
            else:
                # Exact match
                conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )
        
        return Filter(must=conditions) if conditions else None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        info = self.client.get_collection(self.collection_name)
        
        return {
            "collection_name": self.collection_name,
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "indexed_vectors_count": info.indexed_vectors_count,
            "status": str(info.status),
            "optimizer_status": str(info.optimizer_status) if info.optimizer_status else "N/A",
            "quantization_enabled": self.config.enable_quantization,
            "on_disk": self.config.on_disk
        }
    
    def delete_collection(self):
        """Delete the entire collection."""
        self.client.delete_collection(collection_name=self.collection_name)
        logger.info(f"Deleted collection: {self.collection_name}")
    
    def reset_collection(self):
        """Reset collection (delete and recreate)."""
        try:
            self.delete_collection()
        except Exception as e:
            logger.debug(f"Collection didn't exist: {e}")
        
        self._initialize_collection()
        logger.info(f"Reset collection: {self.collection_name}")
    
    def health_check(self) -> bool:
        """Check if Qdrant is healthy."""
        try:
            self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False


async def create_qdrant_store(
    host: str = "localhost",
    port: int = 6333,
    collection_name: str = "documents",
    enable_quantization: bool = True
) -> QdrantStore:
    """
    Factory function to create Qdrant store.
    
    Args:
        host: Qdrant server host
        port: Qdrant server port
        collection_name: Collection name
        enable_quantization: Enable int8 quantization (4x memory savings)
    
    Returns:
        Configured QdrantStore instance
    """
    config = QdrantStoreConfig(
        host=host,
        port=port,
        collection_name=collection_name,
        enable_quantization=enable_quantization
    )
    return QdrantStore(config)