"""
CrossEncoder reranking for improved search quality.

This module provides reranking capabilities using sentence-transformers CrossEncoder.
Reranking improves search quality by 20-30% by scoring query-document pairs precisely.

Architecture:
1. Initial retrieval: Fast vector similarity (Jina AI) → top 50-100 candidates
2. Reranking: Precise CrossEncoder scoring → top 5-10 results
3. Result: Better relevance with minimal latency increase

Benefits:
- 20-30% better search quality (BEIR benchmark)
- Works with existing embeddings (no reindexing)
- Fast (only reranks small candidate set)
- Easy to integrate (drop-in enhancement)
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)


@dataclass
class RerankerConfig:
    """Configuration for CrossEncoder reranking."""
    model_name: str = "cross-encoder/ms-marco-MiniLM-L6-v2"
    """
    Recommended models:
    - cross-encoder/ms-marco-MiniLM-L6-v2: Fast, general purpose (default)
    - cross-encoder/ms-marco-TinyBERT-L-2-v2: Fastest, smaller model
    - cross-encoder/mmarco-mMiniLMv2-L12-H384-v1: Multilingual support
    - cross-encoder/ms-marco-MiniLM-L-12-v2: Better quality, slower
    """
    
    batch_size: int = 32
    """Batch size for reranking (higher = faster, more memory)"""
    
    show_progress: bool = False
    """Show progress bar during reranking"""
    
    activation_function: Optional[str] = None
    """Activation function (None = model default, 'sigmoid' for probabilities)"""


class SentenceTransformerReranker:
    """
    CrossEncoder reranker for improving search quality.
    
    CrossEncoders are more accurate than bi-encoders (like Jina AI) because they:
    - Process query + document together (not separately)
    - Capture fine-grained interactions between query and document
    - Output precise relevance scores
    
    However, they're slower, so we only use them on a small candidate set.
    
    Example:
        >>> reranker = SentenceTransformerReranker()
        >>> results = await reranker.rerank(
        ...     query="How to deploy to Vercel?",
        ...     candidates=initial_search_results,
        ...     top_k=5
        ... )
    """
    
    def __init__(self, config: Optional[RerankerConfig] = None):
        """
        Initialize CrossEncoder reranker.
        
        Args:
            config: Reranker configuration (uses defaults if None)
        """
        self.config = config or RerankerConfig()
        
        logger.info(f"Loading CrossEncoder model: {self.config.model_name}")
        try:
            self.model = CrossEncoder(
                self.config.model_name,
                max_length=512,  # Standard max length for most models
                device=None  # Auto-detect (CUDA if available)
            )
            logger.info(f"CrossEncoder loaded successfully on device: {self.model.device}")
        except Exception as e:
            logger.error(f"Failed to load CrossEncoder: {e}")
            raise
    
    async def rerank(
        self,
        query: str,
        candidates: List[Dict[str, Any]],
        top_k: Optional[int] = None,
        return_scores: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Rerank candidates using CrossEncoder.
        
        Args:
            query: Search query
            candidates: List of candidate results from initial retrieval
                       Each candidate should have at least a 'content' or 'text' field
            top_k: Number of top results to return (None = all candidates)
            return_scores: Include reranking scores in results
            
        Returns:
            List of reranked candidates, sorted by relevance score
            
        Example:
            >>> candidates = [
            ...     {"content": "Deploy with Vercel CLI...", "metadata": {...}},
            ...     {"content": "Deploy with Netlify...", "metadata": {...}},
            ... ]
            >>> reranked = await reranker.rerank(
            ...     query="How to deploy to Vercel?",
            ...     candidates=candidates,
            ...     top_k=5
            ... )
        """
        if not candidates:
            logger.warning("No candidates to rerank")
            return []
        
        if not query.strip():
            logger.warning("Empty query, returning candidates as-is")
            return candidates[:top_k] if top_k else candidates
        
        # Extract text from candidates
        documents = []
        for candidate in candidates:
            # Try different common field names
            text = (
                candidate.get("content") or 
                candidate.get("text") or 
                candidate.get("document") or 
                str(candidate)
            )
            documents.append(text)
        
        try:
            # Use CrossEncoder.rank() for efficient reranking
            # This method handles batching and returns sorted results
            if top_k is None:
                top_k = len(documents)
            
            logger.debug(f"Reranking {len(documents)} candidates for query: {query[:50]}...")
            
            ranked_results = self.model.rank(
                query=query,
                documents=documents,
                top_k=min(top_k, len(documents)),
                return_documents=False,  # We'll merge with original candidates
                batch_size=self.config.batch_size,
                show_progress_bar=self.config.show_progress,
                activation_fct=self.config.activation_function
            )
            
            # Merge reranking scores with original candidates
            reranked_candidates = []
            for ranked in ranked_results:
                corpus_id = ranked['corpus_id']
                score = ranked['score']
                
                # Get original candidate
                original = candidates[corpus_id].copy()
                
                # Add reranking score
                if return_scores:
                    original['rerank_score'] = float(score)
                    # Keep original similarity score if it exists
                    if 'score' in original:
                        original['initial_score'] = original['score']
                    original['score'] = float(score)  # Replace with rerank score
                
                reranked_candidates.append(original)
            
            logger.info(
                f"Reranked {len(documents)} candidates → {len(reranked_candidates)} results "
                f"(top score: {reranked_candidates[0]['rerank_score']:.4f})"
            )
            
            return reranked_candidates
            
        except Exception as e:
            logger.error(f"Reranking failed: {e}, returning original candidates")
            return candidates[:top_k] if top_k else candidates
    
    async def score_pairs(
        self,
        query: str,
        documents: List[str]
    ) -> List[float]:
        """
        Score query-document pairs without sorting.
        
        Args:
            query: Search query
            documents: List of documents to score
            
        Returns:
            List of relevance scores (same order as input documents)
            
        Example:
            >>> scores = await reranker.score_pairs(
            ...     query="What is RAG?",
            ...     documents=["RAG is...", "Vector search is...", "LLMs are..."]
            ... )
            >>> # [0.95, 0.42, 0.31]
        """
        if not documents:
            return []
        
        try:
            # Create query-document pairs
            pairs = [[query, doc] for doc in documents]
            
            # Score pairs
            scores = self.model.predict(
                pairs,
                batch_size=self.config.batch_size,
                show_progress_bar=self.config.show_progress,
                activation_fct=self.config.activation_function
            )
            
            return scores.tolist() if hasattr(scores, 'tolist') else list(scores)
            
        except Exception as e:
            logger.error(f"Scoring failed: {e}")
            return [0.0] * len(documents)


# Singleton instance for easy import
_default_reranker: Optional[SentenceTransformerReranker] = None


def get_reranker(config: Optional[RerankerConfig] = None) -> SentenceTransformerReranker:
    """
    Get or create singleton reranker instance.
    
    Args:
        config: Reranker configuration (only used on first call)
        
    Returns:
        Reranker instance
    """
    global _default_reranker
    
    if _default_reranker is None:
        _default_reranker = SentenceTransformerReranker(config)
    
    return _default_reranker
