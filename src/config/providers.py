"""
Simplified provider configuration for OpenAI models.

COPIED AND REFACTORED FROM: ottomator-agents/docling-rag-agent/utils/providers.py

Provides flexible LLM and embedding client creation with environment-based configuration.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ProviderConfig(BaseModel):
    """
    Provider configuration (Pydantic model for validation).
    
    REFACTORED: Added Pydantic model for configuration validation.
    """
    llm_provider: str = Field(default="openai", description="LLM provider")
    llm_model: str = Field(default="gpt-4o-mini", description="LLM model name")
    embedding_provider: str = Field(default="openai", description="Embedding provider")
    embedding_model: str = Field(
        default="text-embedding-3-small", 
        description="Embedding model name"
    )
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    
    @classmethod
    def from_env(cls) -> "ProviderConfig":
        """Create configuration from environment variables."""
        return cls(
            llm_provider=os.getenv('LLM_PROVIDER', 'openai'),
            llm_model=os.getenv('LLM_MODEL', 'gpt-4o-mini'),
            embedding_provider=os.getenv('EMBEDDING_PROVIDER', 'openai'),
            embedding_model=os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small'),
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
        )


def get_llm_model() -> OpenAIModel:
    """
    Get LLM model configuration for OpenAI.
    
    Returns:
        Configured OpenAI model
    """
    config = ProviderConfig.from_env()
    
    if not config.openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    return OpenAIModel(
        config.llm_model, 
        provider=OpenAIProvider(api_key=config.openai_api_key)
    )


def get_embedding_client() -> openai.AsyncOpenAI:
    """
    Get OpenAI client for embeddings.
    
    Returns:
        Configured OpenAI async client for embeddings
    """
    config = ProviderConfig.from_env()
    
    if not config.openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    return openai.AsyncOpenAI(api_key=config.openai_api_key)


def get_embedding_model() -> str:
    """
    Get embedding model name.
    
    Returns:
        Embedding model name
    """
    config = ProviderConfig.from_env()
    return config.embedding_model


def get_ingestion_model() -> OpenAIModel:
    """
    Get model for ingestion tasks (uses same model as main LLM).
    
    Returns:
        Configured model for ingestion tasks
    """
    return get_llm_model()


def validate_configuration() -> bool:
    """
    Validate that required environment variables are set.
    
    Returns:
        True if configuration is valid
    """
    try:
        config = ProviderConfig.from_env()
        
        # Check OpenAI key if using OpenAI
        if config.llm_provider == "openai" and not config.openai_api_key:
            print("Missing OPENAI_API_KEY for OpenAI provider")
            return False
        
        return True
        
    except Exception as e:
        print(f"Configuration validation failed: {e}")
        return False


def get_model_info() -> dict:
    """
    Get information about current model configuration.
    
    Returns:
        Dictionary with model configuration info
    """
    config = ProviderConfig.from_env()
    return {
        "llm_provider": config.llm_provider,
        "llm_model": config.llm_model,
        "embedding_provider": config.embedding_provider,
        "embedding_model": config.embedding_model,
    }
