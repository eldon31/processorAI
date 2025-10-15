"""Agent module - Pydantic AI conversational agent with RAG tools."""

from .agent import rag_agent, AgentDependencies, run_agent_query
from .prompts import SYSTEM_PROMPT
from .tools import (
    VectorSearchInput,
    GraphSearchInput,
    HybridSearchInput,
    DocumentInput,
    DocumentListInput,
    EntityRelationshipInput,
    EntityTimelineInput,
    vector_search_tool,
    graph_search_tool,
    hybrid_search_tool,
    get_document_tool,
    list_documents_tool,
    get_entity_relationships_tool,
    get_entity_timeline_tool,
    perform_comprehensive_search,
)

__all__ = [
    # Agent
    "rag_agent",
    "AgentDependencies",
    "run_agent_query",
    # Prompts
    "SYSTEM_PROMPT",
    # Tool inputs
    "VectorSearchInput",
    "GraphSearchInput",
    "HybridSearchInput",
    "DocumentInput",
    "DocumentListInput",
    "EntityRelationshipInput",
    "EntityTimelineInput",
    # Tool functions
    "vector_search_tool",
    "graph_search_tool",
    "hybrid_search_tool",
    "get_document_tool",
    "list_documents_tool",
    "get_entity_relationships_tool",
    "get_entity_timeline_tool",
    "perform_comprehensive_search",
]
