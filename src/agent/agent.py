"""
Main Pydantic AI agent for agentic RAG with knowledge graph.

REFACTORED from: agentic-rag-knowledge-graph/agent/agent.py
Changes:
- Updated imports to use new module structure
- Will use Chroma MCP client instead of PostgreSQL
- Maintained all Pydantic AI agent functionality
- Added proper type hints and Pydantic models
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from pydantic_ai import Agent, RunContext

from .prompts import SYSTEM_PROMPT
from .tools import (
    vector_search_tool,
    graph_search_tool,
    hybrid_search_tool,
    get_document_tool,
    list_documents_tool,
    get_entity_relationships_tool,
    get_entity_timeline_tool,
    VectorSearchInput,
    GraphSearchInput,
    HybridSearchInput,
    DocumentInput,
    DocumentListInput,
    EntityRelationshipInput,
    EntityTimelineInput,
)
from ..config.providers import get_llm_model

logger = logging.getLogger(__name__)


@dataclass
class AgentDependencies:
    """Dependencies for the RAG agent."""
    session_id: str
    user_id: Optional[str] = None
    search_preferences: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize default search preferences if not provided."""
        if not self.search_preferences:
            self.search_preferences = {
                "use_vector": True,
                "use_graph": True,
                "default_limit": 10
            }


# Initialize the agent with configured LLM model
rag_agent = Agent(
    get_llm_model(),
    deps_type=AgentDependencies,
    system_prompt=SYSTEM_PROMPT
)


# Register tools with proper docstrings
@rag_agent.tool
async def vector_search(
    ctx: RunContext[AgentDependencies],
    query: str,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Search for relevant information using semantic similarity.
    
    This tool performs vector similarity search across document chunks
    to find semantically related content. Returns the most relevant results
    based on embedding similarity.
    
    Args:
        query: Search query to find similar content
        limit: Maximum number of results to return (1-50)
    
    Returns:
        List of matching chunks ordered by similarity (best first)
    """
    input_data = VectorSearchInput(query=query, limit=limit)
    results = await vector_search_tool(input_data)
    return results


@rag_agent.tool
async def graph_search(
    ctx: RunContext[AgentDependencies],
    query: str
) -> List[Dict[str, Any]]:
    """
    Search the knowledge graph for facts and relationships.
    
    This tool queries the Graphiti knowledge graph to find specific facts,
    relationships between entities, and temporal information. Best for
    understanding entity relationships and fact verification.
    
    Args:
        query: Search query to find facts and relationships
    
    Returns:
        List of facts with temporal data and entity relationships
    """
    input_data = GraphSearchInput(query=query)
    results = await graph_search_tool(input_data)
    return results


@rag_agent.tool
async def hybrid_search(
    ctx: RunContext[AgentDependencies],
    query: str,
    limit: int = 10,
    text_weight: float = 0.3
) -> List[Dict[str, Any]]:
    """
    Perform both vector and keyword search for comprehensive results.
    
    This tool combines semantic similarity search with keyword matching
    for the best coverage. It ranks results using both vector similarity
    and text matching scores.
    
    Args:
        query: Search query for hybrid search
        limit: Maximum number of results to return (1-50)
        text_weight: Weight for text similarity vs vector similarity (0.0-1.0)
    
    Returns:
        List of chunks ranked by combined relevance score
    """
    input_data = HybridSearchInput(
        query=query,
        limit=limit,
        text_weight=text_weight
    )
    results = await hybrid_search_tool(input_data)
    return results


@rag_agent.tool
async def get_document(
    ctx: RunContext[AgentDependencies],
    document_id: str
) -> Optional[Dict[str, Any]]:
    """
    Retrieve the complete content of a specific document.
    
    This tool fetches the full document content along with all its chunks
    and metadata. Best for getting comprehensive information from a specific
    source when you need the complete context.
    
    Args:
        document_id: UUID of the document to retrieve
    
    Returns:
        Complete document data with content and metadata, or None if not found
    """
    input_data = DocumentInput(document_id=document_id)
    document = await get_document_tool(input_data)
    
    if document:
        return {
            "id": document["id"],
            "title": document["title"],
            "source": document["source"],
            "content": document["content"],
            "chunk_count": len(document.get("chunks", [])),
            "created_at": document["created_at"]
        }
    
    return None


@rag_agent.tool
async def list_documents(
    ctx: RunContext[AgentDependencies],
    limit: int = 20,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    List available documents with their metadata.
    
    This tool provides an overview of all documents in the knowledge base,
    including titles, sources, and chunk counts. Best for understanding
    what information sources are available.
    
    Args:
        limit: Maximum number of documents to return (1-100)
        offset: Number of documents to skip for pagination
    
    Returns:
        List of documents with metadata and chunk counts
    """
    input_data = DocumentListInput(limit=limit, offset=offset)
    documents = await list_documents_tool(input_data)
    return documents


@rag_agent.tool
async def get_entity_relationships(
    ctx: RunContext[AgentDependencies],
    entity_name: str,
    depth: int = 2
) -> Dict[str, Any]:
    """
    Get all relationships for a specific entity in the knowledge graph.
    
    This tool explores the Graphiti knowledge graph to find how a specific
    entity relates to other entities through semantic search. Best for
    understanding entity connections and relationships.
    
    Args:
        entity_name: Name of the entity to explore (e.g., "Google", "OpenAI")
        depth: Maximum traversal depth for relationships (1-5)
    
    Returns:
        Entity relationships and connected facts with relationship types
    """
    input_data = EntityRelationshipInput(
        entity_name=entity_name,
        depth=depth
    )
    return await get_entity_relationships_tool(input_data)


@rag_agent.tool
async def get_entity_timeline(
    ctx: RunContext[AgentDependencies],
    entity_name: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get the timeline of facts for a specific entity.
    
    This tool retrieves chronological information about an entity,
    showing how information has evolved over time. Best for understanding
    temporal aspects of entity information.
    
    Args:
        entity_name: Name of the entity (e.g., "Microsoft", "AI")
        start_date: Start date in ISO format (YYYY-MM-DD), optional
        end_date: End date in ISO format (YYYY-MM-DD), optional
    
    Returns:
        Chronological list of facts about the entity with timestamps
    """
    input_data = EntityTimelineInput(
        entity_name=entity_name,
        start_date=start_date,
        end_date=end_date
    )
    return await get_entity_timeline_tool(input_data)


async def run_agent_query(
    query: str,
    session_id: str,
    user_id: Optional[str] = None,
    search_preferences: Optional[Dict[str, Any]] = None
) -> str:
    """
    Run a query through the RAG agent.
    
    Args:
        query: User query
        session_id: Session identifier for conversation tracking
        user_id: Optional user identifier
        search_preferences: Optional search preferences
    
    Returns:
        Agent response as string
    """
    deps = AgentDependencies(
        session_id=session_id,
        user_id=user_id,
        search_preferences=search_preferences or {}
    )
    
    try:
        result = await rag_agent.run(query, deps=deps)
        # PydanticAI's result is the actual response (not result.data)
        return str(result)
    except Exception as e:
        logger.error(f"Agent query failed: {e}")
        return f"Error processing query: {str(e)}"
