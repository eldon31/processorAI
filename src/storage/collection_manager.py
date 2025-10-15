"""
Multi-collection manager for Chroma vector database.

Manages multiple collections for different knowledge categories:
- Programming languages (Python, JavaScript, etc.)
- Documentation types (API docs, tool docs, etc.)
- Domain knowledge (algorithms, system design, etc.)
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

import chromadb
from chromadb.config import Settings

from src.models.collection import (
    CollectionCategory,
    CollectionConfig,
    CollectionMetadata,
    PREDEFINED_COLLECTIONS,
    get_collection_config,
)
from src.storage.chroma_client import ChromaConfig, SearchResult

logger = logging.getLogger(__name__)


class MultiCollectionManager:
    """
    Manager for multiple Chroma collections.
    
    Provides:
    - Auto-routing to appropriate collection based on content type
    - Cross-collection search
    - Collection lifecycle management
    - Statistics and monitoring
    """
    
    def __init__(self, config: Optional[ChromaConfig] = None):
        """
        Initialize multi-collection manager.
        
        Args:
            config: Chroma configuration
        """
        self.config = config or ChromaConfig.from_env()
        self._client: Optional[chromadb.Client] = None
        self._collections: Dict[str, chromadb.Collection] = {}
        self._metadata: Dict[str, CollectionMetadata] = {}
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize Chroma client and load existing collections."""
        if self._initialized:
            return
        
        try:
            # Create HTTP client
            if self.config.persist_directory:
                self._client = chromadb.PersistentClient(
                    path=self.config.persist_directory,
                    settings=Settings(
                        anonymized_telemetry=False,
                        allow_reset=False
                    )
                )
                logger.info(f"Initialized Chroma persistent client at {self.config.persist_directory}")
            else:
                self._client = chromadb.HttpClient(
                    host=self.config.host,
                    port=self.config.port,
                    settings=Settings(
                        anonymized_telemetry=False,
                        allow_reset=False
                    )
                )
                logger.info(f"Initialized Chroma HTTP client at {self.config.host}:{self.config.port}")
            
            # Load existing collections
            await self._load_collections()
            
            self._initialized = True
            logger.info(f"Multi-collection manager ready with {len(self._collections)} collections")
            
        except Exception as e:
            logger.error(f"Failed to initialize multi-collection manager: {e}")
            raise
    
    async def _load_collections(self) -> None:
        """Load existing collections from Chroma."""
        try:
            collections = self._client.list_collections()
            
            for collection in collections:
                self._collections[collection.name] = collection
                
                # Extract metadata
                metadata = collection.metadata or {}
                category = metadata.get("category", CollectionCategory.GENERAL.value)
                
                self._metadata[collection.name] = CollectionMetadata(
                    category=CollectionCategory(category),
                    description=metadata.get("description", ""),
                    tags=metadata.get("tags", "").split(",") if metadata.get("tags") else [],
                    language=metadata.get("language"),
                    framework=metadata.get("framework"),
                    version=metadata.get("version"),
                    document_count=collection.count(),
                    chunk_count=collection.count(),
                )
            
            logger.info(f"Loaded {len(self._collections)} existing collections")
            
        except Exception as e:
            logger.warning(f"Error loading collections: {e}")
    
    async def create_collection(
        self,
        config: CollectionConfig
    ) -> chromadb.Collection:
        """
        Create a new collection with specified configuration.
        
        Args:
            config: Collection configuration
            
        Returns:
            Created Chroma collection
        """
        if not self._initialized:
            await self.initialize()
        
        try:
            # Prepare metadata
            metadata = config.to_chroma_metadata()
            
            # Create collection
            collection = self._client.get_or_create_collection(
                name=config.name,
                metadata=metadata
            )
            
            # Cache collection
            self._collections[config.name] = collection
            self._metadata[config.name] = CollectionMetadata(
                category=config.category,
                description=config.description,
                tags=config.tags,
                language=config.language,
                framework=config.framework,
                version=config.version,
            )
            
            logger.info(f"Created collection: {config.name} ({config.category.value})")
            return collection
            
        except Exception as e:
            logger.error(f"Failed to create collection {config.name}: {e}")
            raise
    
    async def get_or_create_collection(
        self,
        category: Optional[CollectionCategory] = None,
        language: Optional[str] = None,
        framework: Optional[str] = None,
        custom_name: Optional[str] = None,
    ) -> chromadb.Collection:
        """
        Get existing collection or create new one.
        
        Args:
            category: Collection category
            language: Programming language (for code collections)
            framework: Framework name (for framework docs)
            custom_name: Custom collection name (overrides other params)
            
        Returns:
            Chroma collection
        """
        if not self._initialized:
            await self.initialize()
        
        # Determine collection name
        if custom_name:
            collection_name = custom_name
        elif category:
            collection_name = category.value
        elif language:
            collection_name = f"{language.lower()}_code"
        elif framework:
            collection_name = CollectionCategory.FRAMEWORK_DOCS.value
        else:
            collection_name = CollectionCategory.GENERAL.value
        
        # Return existing if available
        if collection_name in self._collections:
            return self._collections[collection_name]
        
        # Create new collection
        if category and category in PREDEFINED_COLLECTIONS:
            config = PREDEFINED_COLLECTIONS[category]
        else:
            # Create custom config
            config = CollectionConfig(
                name=collection_name,
                category=category or CollectionCategory.GENERAL,
                description=f"Collection for {collection_name}",
                language=language,
                framework=framework,
            )
        
        return await self.create_collection(config)
    
    async def add_to_collection(
        self,
        collection_name: str,
        ids: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
        documents: List[str],
    ) -> None:
        """
        Add embeddings to specified collection.
        
        Args:
            collection_name: Target collection name
            ids: Chunk IDs
            embeddings: Embedding vectors
            metadatas: Chunk metadata
            documents: Chunk text content
        """
        if not self._initialized:
            await self.initialize()
        
        collection = self._collections.get(collection_name)
        if not collection:
            raise ValueError(f"Collection not found: {collection_name}")
        
        # Add in batches
        batch_size = self.config.batch_size
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i:i + batch_size]
            batch_embeddings = embeddings[i:i + batch_size]
            batch_metadatas = metadatas[i:i + batch_size]
            batch_documents = documents[i:i + batch_size]
            
            collection.add(
                ids=batch_ids,
                embeddings=batch_embeddings,
                metadatas=batch_metadatas,
                documents=batch_documents,
            )
        
        logger.info(f"Added {len(ids)} embeddings to collection '{collection_name}'")
    
    async def search_collection(
        self,
        collection_name: str,
        query_embedding: List[float],
        n_results: int = 10,
        where: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """
        Search within a specific collection.
        
        Args:
            collection_name: Collection to search
            query_embedding: Query vector
            n_results: Number of results
            where: Metadata filters
            
        Returns:
            List of search results
        """
        if not self._initialized:
            await self.initialize()
        
        collection = self._collections.get(collection_name)
        if not collection:
            raise ValueError(f"Collection not found: {collection_name}")
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
        )
        
        # Convert to SearchResult objects
        search_results = []
        for i in range(len(results['ids'][0])):
            metadata = results['metadatas'][0][i]
            search_results.append(
                SearchResult(
                    id=results['ids'][0][i],
                    document_id=metadata.get('document_id', ''),
                    content=results['documents'][0][i],
                    score=1.0 - results['distances'][0][i],  # Convert distance to similarity
                    metadata=metadata,
                    document_title=metadata.get('document_title', ''),
                    document_source=metadata.get('source', ''),
                )
            )
        
        return search_results
    
    async def search_all_collections(
        self,
        query_embedding: List[float],
        n_results_per_collection: int = 5,
        categories: Optional[List[CollectionCategory]] = None,
    ) -> Dict[str, List[SearchResult]]:
        """
        Search across multiple collections.
        
        Args:
            query_embedding: Query vector
            n_results_per_collection: Results per collection
            categories: Filter by categories (None = search all)
            
        Returns:
            Dict mapping collection names to search results
        """
        if not self._initialized:
            await self.initialize()
        
        results = {}
        
        for name, collection in self._collections.items():
            # Filter by category if specified
            if categories:
                metadata = self._metadata.get(name)
                if metadata and metadata.category not in categories:
                    continue
            
            try:
                collection_results = await self.search_collection(
                    collection_name=name,
                    query_embedding=query_embedding,
                    n_results=n_results_per_collection,
                )
                results[name] = collection_results
            except Exception as e:
                logger.warning(f"Error searching collection {name}: {e}")
        
        return results
    
    async def list_collections(self) -> List[Dict[str, Any]]:
        """
        List all collections with metadata.
        
        Returns:
            List of collection information
        """
        if not self._initialized:
            await self.initialize()
        
        collections = []
        for name, collection in self._collections.items():
            metadata = self._metadata.get(name)
            collections.append({
                "name": name,
                "category": metadata.category.value if metadata else "unknown",
                "description": metadata.description if metadata else "",
                "document_count": collection.count(),
                "tags": metadata.tags if metadata else [],
                "language": metadata.language if metadata else None,
                "framework": metadata.framework if metadata else None,
            })
        
        return collections
    
    async def delete_collection(self, collection_name: str) -> bool:
        """
        Delete a collection.
        
        Args:
            collection_name: Collection to delete
            
        Returns:
            True if deleted successfully
        """
        if not self._initialized:
            await self.initialize()
        
        try:
            self._client.delete_collection(collection_name)
            self._collections.pop(collection_name, None)
            self._metadata.pop(collection_name, None)
            logger.info(f"Deleted collection: {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete collection {collection_name}: {e}")
            return False
    
    async def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """
        Get statistics for a collection.
        
        Args:
            collection_name: Collection name
            
        Returns:
            Collection statistics
        """
        if not self._initialized:
            await self.initialize()
        
        collection = self._collections.get(collection_name)
        if not collection:
            raise ValueError(f"Collection not found: {collection_name}")
        
        metadata = self._metadata.get(collection_name)
        
        return {
            "name": collection_name,
            "category": metadata.category.value if metadata else "unknown",
            "description": metadata.description if metadata else "",
            "chunk_count": collection.count(),
            "tags": metadata.tags if metadata else [],
            "language": metadata.language if metadata else None,
            "framework": metadata.framework if metadata else None,
            "last_updated": metadata.last_updated if metadata else None,
        }


# Global manager instance
_collection_manager: Optional[MultiCollectionManager] = None


def get_collection_manager() -> MultiCollectionManager:
    """Get or create global collection manager instance."""
    global _collection_manager
    if _collection_manager is None:
        _collection_manager = MultiCollectionManager()
    return _collection_manager


async def initialize_collection_manager() -> None:
    """Initialize global collection manager."""
    manager = get_collection_manager()
    await manager.initialize()


async def close_collection_manager() -> None:
    """Close global collection manager."""
    global _collection_manager
    if _collection_manager:
        # Cleanup if needed
        _collection_manager._initialized = False
        _collection_manager = None
