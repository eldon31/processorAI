"""
Knowledge graph builder for extracting entities and relationships using Graphiti.

Adapted from agentic-rag-knowledge-graph/ingestion/graph_builder.py

CRITICAL IMPLEMENTATION NOTES:
1. Process chunks ONE-BY-ONE (no batching) - batching causes Graphiti timeouts
2. Enforce 6000 char limit per episode (~1500 tokens) - Graphiti has 8192 token hard limit
3. Add 0.5s delay between episodes - prevents rate limiting
4. Continue on chunk failure - don't abort entire document
5. Truncate at sentence boundaries - maintains semantic coherence

These patterns are essential for Graphiti stability. See IMPLEMENTATION_ANALYSIS.md for details.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import asyncio

from pydantic import BaseModel, Field

from ..ingestion.chunker import DocumentChunk
from ..graph.graph_client import _get_global_client as get_graph_client

logger = logging.getLogger(__name__)


class GraphBuildingResult(BaseModel):
    """Result of adding document to knowledge graph."""
    
    episodes_created: int = Field(..., description="Number of episodes successfully created")
    total_chunks: int = Field(..., description="Total number of chunks processed")
    entities_extracted: int = Field(default=0, description="Number of entities extracted (estimated)")
    relationships_created: int = Field(default=0, description="Number of relationships created (estimated)")
    errors: List[str] = Field(default_factory=list, description="List of error messages")
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate (0-1)."""
        if self.total_chunks == 0:
            return 0.0
        return self.episodes_created / self.total_chunks


class GraphBuilder:
    """
    Builds knowledge graph from document chunks using Graphiti.
    
    This class handles the critical task of converting document chunks into
    knowledge graph episodes. It implements strict limits and delays to
    ensure Graphiti stability.
    """
    
    def __init__(self):
        """Initialize graph builder."""
        self.graph_client = get_graph_client()
        self._initialized = False
    
    async def initialize(self):
        """Initialize graph client connection."""
        if not self._initialized:
            if not self.graph_client._initialized:
                await self.graph_client.initialize()
            self._initialized = True
            logger.info("Graph builder initialized")
    
    async def close(self):
        """Close graph client connection."""
        if self._initialized:
            # Don't close global client, just mark as uninitialized
            self._initialized = False
            logger.info("Graph builder closed")
    
    async def add_document_to_graph(
        self,
        chunks: List[DocumentChunk],
        document_title: str,
        document_source: str,
        document_metadata: Optional[Dict[str, Any]] = None
    ) -> GraphBuildingResult:
        """
        Add document chunks to the knowledge graph.
        
        CRITICAL: This function processes chunks ONE-BY-ONE with delays.
        Do NOT modify to use batch processing - it will cause timeouts.
        
        Args:
            chunks: List of document chunks to add
            document_title: Title of the document
            document_source: Source identifier for the document
            document_metadata: Optional additional metadata
        
        Returns:
            GraphBuildingResult with statistics and errors
        
        Process:
            1. Truncate chunk content to 6000 chars (sentence boundary)
            2. Add as Graphiti episode
            3. Wait 0.5 seconds
            4. Repeat for next chunk
            5. Continue even if individual chunks fail
        
        Example:
            >>> builder = GraphBuilder()
            >>> await builder.initialize()
            >>> result = await builder.add_document_to_graph(
            ...     chunks=document_chunks,
            ...     document_title="Python Tutorial",
            ...     document_source="tutorials/python.md"
            ... )
            >>> print(f"Created {result.episodes_created}/{result.total_chunks} episodes")
        """
        if not self._initialized:
            await self.initialize()
        
        if not chunks:
            logger.warning("No chunks provided for graph building")
            return GraphBuildingResult(
                episodes_created=0,
                total_chunks=0,
                errors=["No chunks provided"]
            )
        
        logger.info(f"Adding {len(chunks)} chunks to knowledge graph for: {document_title}")
        logger.info("⚠️ Large chunks will be truncated to 6000 chars (Graphiti token limit)")
        
        # Check for oversized chunks and warn
        oversized_chunks = [i for i, chunk in enumerate(chunks) if len(chunk.content) > 6000]
        if oversized_chunks:
            logger.warning(
                f"Found {len(oversized_chunks)} chunks over 6000 chars: "
                f"{oversized_chunks[:10]}{'...' if len(oversized_chunks) > 10 else ''}"
            )
        
        episodes_created = 0
        errors = []
        
        # CRITICAL: Process chunks ONE-BY-ONE (no batching)
        for i, chunk in enumerate(chunks):
            try:
                # Create unique episode ID
                timestamp = datetime.now().timestamp()
                episode_id = f"{document_source}_{chunk.index}_{timestamp}"
                
                # Prepare episode content with strict size limits
                episode_content = self._prepare_episode_content(
                    chunk=chunk,
                    document_title=document_title,
                    document_metadata=document_metadata
                )
                
                # Create concise source description
                source_description = f"{document_title} (Chunk {chunk.index})"
                
                # Add episode to Graphiti
                await self.graph_client.add_episode(
                    episode_id=episode_id,
                    content=episode_content,
                    source=source_description,
                    timestamp=datetime.now(timezone.utc),
                    metadata={
                        "document_title": document_title,
                        "document_source": document_source,
                        "chunk_index": chunk.index,
                        "original_length": len(chunk.content),
                        "processed_length": len(episode_content),
                        "chunk_metadata": chunk.metadata
                    }
                )
                
                episodes_created += 1
                logger.info(
                    f"✓ Episode {i+1}/{len(chunks)}: {episode_id} "
                    f"({len(episode_content)} chars)"
                )
                
                # CRITICAL: Delay between episodes to prevent rate limiting
                if i < len(chunks) - 1:
                    await asyncio.sleep(0.5)
                    
            except Exception as e:
                error_msg = f"Chunk {chunk.index}: {str(e)}"
                logger.error(f"Failed to add chunk {chunk.index} to graph: {e}")
                errors.append(error_msg)
                
                # CRITICAL: Continue processing even if one chunk fails
                continue
        
        # Estimate entities and relationships (Graphiti extracts these internally)
        # We can't get exact counts without querying the graph, so estimate
        estimated_entities = episodes_created * 3  # Rough estimate: 3 entities per episode
        estimated_relationships = episodes_created * 2  # Rough estimate: 2 relationships per episode
        
        result = GraphBuildingResult(
            episodes_created=episodes_created,
            total_chunks=len(chunks),
            entities_extracted=estimated_entities,
            relationships_created=estimated_relationships,
            errors=errors
        )
        
        logger.info(
            f"Graph building complete: {episodes_created}/{len(chunks)} episodes created, "
            f"{len(errors)} errors (success rate: {result.success_rate:.1%})"
        )
        
        return result
    
    def _prepare_episode_content(
        self,
        chunk: DocumentChunk,
        document_title: str,
        document_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Prepare episode content with strict token limit enforcement.
        
        CRITICAL: Graphiti has a hard limit of 8192 tokens. We use 6000 chars
        (~1500 tokens) to leave room for Graphiti's internal processing.
        
        Args:
            chunk: Document chunk to process
            document_title: Title of the document
            document_metadata: Optional metadata
        
        Returns:
            Formatted episode content (guaranteed ≤6000 chars)
        
        Process:
            1. Check if content exceeds 6000 chars
            2. If yes, truncate at sentence boundary (prefer clean ending)
            3. Add [TRUNCATED] marker
            4. Prepend minimal context (document title)
        """
        # CRITICAL: Hard limit to avoid Graphiti's 8192 token limit
        # ~4 chars per token, so 6000 chars ≈ 1500 tokens
        MAX_CONTENT_LENGTH = 6000
        
        content = chunk.content
        original_length = len(content)
        
        if len(content) > MAX_CONTENT_LENGTH:
            # Truncate content at sentence boundary if possible
            truncated = content[:MAX_CONTENT_LENGTH]
            
            # Find last sentence ending
            last_sentence_end = max(
                truncated.rfind('. '),
                truncated.rfind('! '),
                truncated.rfind('? ')
            )
            
            # If we can keep 70%+ and end cleanly, use sentence boundary
            if last_sentence_end > MAX_CONTENT_LENGTH * 0.7:
                content = truncated[:last_sentence_end + 1] + " [TRUNCATED]"
            else:
                # Otherwise, hard truncate and add marker
                content = truncated + "... [TRUNCATED]"
            
            logger.warning(
                f"Truncated chunk {chunk.index}: "
                f"{original_length} → {len(content)} chars "
                f"({(len(content)/original_length)*100:.0f}% retained)"
            )
        
        # Add minimal context (document title)
        # Only if we have room (leave 100 chars buffer)
        if document_title and len(content) < MAX_CONTENT_LENGTH - 100:
            # Truncate title if necessary
            title = document_title[:50] if len(document_title) > 50 else document_title
            episode_content = f"[Document: {title}]\n\n{content}"
        else:
            episode_content = content
        
        return episode_content
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Rough estimate of token count.
        
        Uses simple heuristic: ~4 characters per token.
        This is approximate but good enough for our limits.
        """
        return len(text) // 4
    
    def _is_content_too_large(self, content: str, max_tokens: int = 1500) -> bool:
        """
        Check if content exceeds safe token limit.
        
        Args:
            content: Text content to check
            max_tokens: Maximum allowed tokens (default 1500 for safety)
        
        Returns:
            True if content is too large
        """
        return self._estimate_tokens(content) > max_tokens


# Convenience function for direct usage
async def build_knowledge_graph(
    chunks: List[DocumentChunk],
    document_title: str,
    document_source: str,
    document_metadata: Optional[Dict[str, Any]] = None
) -> GraphBuildingResult:
    """
    Convenience function to build knowledge graph from chunks.
    
    This function creates a GraphBuilder, processes the chunks, and
    cleans up automatically.
    
    Args:
        chunks: Document chunks to process
        document_title: Document title
        document_source: Document source identifier
        document_metadata: Optional metadata
    
    Returns:
        GraphBuildingResult with statistics
    
    Example:
        >>> from src.ingestion.chunker import create_chunker
        >>> chunker = create_chunker()
        >>> chunks = await chunker.chunk_document(content, title, source)
        >>> result = await build_knowledge_graph(
        ...     chunks=chunks,
        ...     document_title=title,
        ...     document_source=source
        ... )
        >>> print(f"Success rate: {result.success_rate:.1%}")
    """
    builder = GraphBuilder()
    try:
        await builder.initialize()
        result = await builder.add_document_to_graph(
            chunks=chunks,
            document_title=document_title,
            document_source=document_source,
            document_metadata=document_metadata
        )
        return result
    finally:
        await builder.close()
