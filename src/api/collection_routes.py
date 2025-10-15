"""
Enhanced API routes with multi-collection support.

Extends the base routes with collection-specific endpoints.
"""

from typing import Optional, List
from fastapi import APIRouter, Query as FastAPIQuery

from src.storage.collection_manager import get_collection_manager
from src.models.collection import CollectionCategory


collection_router = APIRouter(prefix="/api/v1/collections", tags=["Collections"])


@collection_router.get("/")
async def list_all_collections():
    """
    List all available collections.
    
    Returns:
        List of collections with metadata
    """
    manager = get_collection_manager()
    collections = await manager.list_collections()
    
    return {
        "collections": collections,
        "total": len(collections),
    }


@collection_router.post("/create")
async def create_new_collection(
    name: str,
    category: CollectionCategory,
    description: str,
    language: Optional[str] = None,
    framework: Optional[str] = None,
    tags: List[str] = [],
):
    """
    Create a new collection.
    
    Args:
        name: Collection name (unique)
        category: Collection category
        description: Collection description
        language: Programming language (optional)
        framework: Framework name (optional)
        tags: Searchable tags (optional)
        
    Returns:
        Created collection information
    """
    from src.models.collection import CollectionConfig
    
    manager = get_collection_manager()
    
    config = CollectionConfig(
        name=name,
        category=category,
        description=description,
        language=language,
        framework=framework,
        tags=tags,
    )
    
    collection = await manager.create_collection(config)
    
    return {
        "name": name,
        "category": category.value,
        "description": description,
        "status": "created",
        "count": collection.count(),
    }


@collection_router.get("/{collection_name}/stats")
async def get_collection_statistics(collection_name: str):
    """
    Get statistics for a specific collection.
    
    Args:
        collection_name: Collection name
        
    Returns:
        Collection statistics
    """
    manager = get_collection_manager()
    stats = await manager.get_collection_stats(collection_name)
    
    return stats


@collection_router.delete("/{collection_name}")
async def delete_collection_endpoint(collection_name: str):
    """
    Delete a collection and all its data.
    
    Args:
        collection_name: Collection to delete
        
    Returns:
        Deletion confirmation
    """
    manager = get_collection_manager()
    success = await manager.delete_collection(collection_name)
    
    if success:
        return {
            "status": "success",
            "message": f"Collection '{collection_name}' deleted",
        }
    else:
        return {
            "status": "error",
            "message": f"Failed to delete collection '{collection_name}'",
        }


@collection_router.post("/search")
async def search_across_collections(
    query: str,
    categories: Optional[List[CollectionCategory]] = None,
    n_results_per_collection: int = 5,
):
    """
    Search across multiple collections.
    
    Args:
        query: Search query
        categories: Filter by categories (None = search all)
        n_results_per_collection: Results per collection
        
    Returns:
        Search results grouped by collection
    """
    from src.ingestion.embedder import create_embedder
    
    # Generate query embedding
    embedder = create_embedder()
    query_embedding = await embedder.embed_query(query)
    
    # Search across collections
    manager = get_collection_manager()
    results = await manager.search_all_collections(
        query_embedding=query_embedding,
        n_results_per_collection=n_results_per_collection,
        categories=categories,
    )
    
    # Format response
    formatted_results = {}
    total_results = 0
    
    for collection_name, collection_results in results.items():
        formatted_results[collection_name] = [
            {
                "chunk_id": r.id,
                "content": r.content[:200] + "..." if len(r.content) > 200 else r.content,
                "score": r.score,
                "document_title": r.document_title,
                "document_source": r.document_source,
            }
            for r in collection_results
        ]
        total_results += len(collection_results)
    
    return {
        "query": query,
        "results": formatted_results,
        "total_results": total_results,
        "collections_searched": len(results),
    }


@collection_router.get("/categories")
async def list_collection_categories():
    """
    List all available collection categories.
    
    Returns:
        Available categories with descriptions
    """
    from src.models.collection import PREDEFINED_COLLECTIONS
    
    categories = []
    for category, config in PREDEFINED_COLLECTIONS.items():
        categories.append({
            "category": category.value,
            "name": config.name,
            "description": config.description,
            "tags": config.tags,
            "language": config.language,
        })
    
    return {
        "categories": categories,
        "total": len(categories),
    }
