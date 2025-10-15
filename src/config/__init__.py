"""
Configuration package for Universal File-to-Knowledge Converter.

Provides environment-based configuration for LLM providers, embedding models, and settings.
"""

from src.config.providers import (
    ProviderConfig,
    get_llm_model,
    get_embedding_client,
    get_embedding_model,
    get_ingestion_model,
    validate_configuration,
    get_model_info,
)

__all__ = [
    "ProviderConfig",
    "get_llm_model",
    "get_embedding_client",
    "get_embedding_model",
    "get_ingestion_model",
    "validate_configuration",
    "get_model_info",
]
