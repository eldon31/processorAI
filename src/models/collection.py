"""
Collection categories for organizing different types of knowledge.

Each collection represents a specialized knowledge domain with tailored metadata.
"""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class CollectionCategory(str, Enum):
    """Predefined collection categories for knowledge organization."""
    
    # Programming Languages
    PYTHON = "python_code"
    JAVASCRIPT = "javascript_code"
    TYPESCRIPT = "typescript_code"
    JAVA = "java_code"
    CPP = "cpp_code"
    RUST = "rust_code"
    GO = "go_code"
    
    # Documentation Types
    API_DOCS = "api_documentation"
    TOOL_DOCS = "tool_implementation"
    FRAMEWORK_DOCS = "framework_documentation"
    LIBRARY_DOCS = "library_documentation"
    
    # Domain Knowledge
    ALGORITHMS = "algorithms_datastructures"
    SYSTEM_DESIGN = "system_design"
    DATABASE = "database_design"
    DEVOPS = "devops_infrastructure"
    SECURITY = "security_practices"
    
    # Project-Specific
    REQUIREMENTS = "project_requirements"
    ARCHITECTURE = "architecture_docs"
    TUTORIALS = "tutorials_guides"
    TROUBLESHOOTING = "troubleshooting_faq"
    
    # General
    GENERAL = "general_knowledge"
    RESEARCH_PAPERS = "research_papers"
    BLOG_POSTS = "blog_posts"
    
    @classmethod
    def from_file_extension(cls, extension: str) -> "CollectionCategory":
        """Determine collection category from file extension."""
        extension = extension.lower().lstrip('.')
        
        # Code files
        code_mapping = {
            'py': cls.PYTHON,
            'js': cls.JAVASCRIPT,
            'ts': cls.TYPESCRIPT,
            'tsx': cls.TYPESCRIPT,
            'jsx': cls.JAVASCRIPT,
            'java': cls.JAVA,
            'cpp': cls.CPP,
            'cc': cls.CPP,
            'cxx': cls.CPP,
            'rs': cls.RUST,
            'go': cls.GO,
        }
        
        if extension in code_mapping:
            return code_mapping[extension]
        
        # Default to general
        return cls.GENERAL
    
    @classmethod
    def from_content_type(cls, content_type: Optional[str]) -> "CollectionCategory":
        """Determine collection from content analysis."""
        if not content_type:
            return cls.GENERAL
        
        content_type = content_type.lower()
        
        if 'api' in content_type:
            return cls.API_DOCS
        elif 'tool' in content_type or 'implementation' in content_type:
            return cls.TOOL_DOCS
        elif 'framework' in content_type:
            return cls.FRAMEWORK_DOCS
        elif 'algorithm' in content_type:
            return cls.ALGORITHMS
        elif 'architecture' in content_type:
            return cls.ARCHITECTURE
        elif 'tutorial' in content_type or 'guide' in content_type:
            return cls.TUTORIALS
        elif 'security' in content_type:
            return cls.SECURITY
        
        return cls.GENERAL


class CollectionMetadata(BaseModel):
    """Metadata schema for a collection."""
    
    category: CollectionCategory
    description: str = Field(..., description="Collection purpose and content")
    tags: list[str] = Field(default_factory=list, description="Searchable tags")
    language: Optional[str] = Field(None, description="Primary programming language (if applicable)")
    framework: Optional[str] = Field(None, description="Framework/tool name (if applicable)")
    version: Optional[str] = Field(None, description="Version information (if applicable)")
    
    # Collection statistics
    document_count: int = Field(default=0, ge=0)
    chunk_count: int = Field(default=0, ge=0)
    last_updated: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True


class CollectionConfig(BaseModel):
    """Configuration for creating/managing a Chroma collection."""
    
    name: str = Field(..., description="Collection name (unique identifier)")
    category: CollectionCategory
    description: str = Field(..., description="Collection description")
    
    # Optional metadata
    tags: list[str] = Field(default_factory=list)
    language: Optional[str] = None
    framework: Optional[str] = None
    version: Optional[str] = None
    
    # HNSW Configuration (can be customized per collection)
    hnsw_m: int = Field(default=16, ge=4, le=64)
    hnsw_ef_construction: int = Field(default=200, ge=100, le=512)
    hnsw_ef_search: int = Field(default=100, ge=10, le=512)
    
    # Distance metric
    distance_metric: str = Field(default="cosine", description="cosine, l2, or ip")
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
    
    def to_chroma_metadata(self) -> Dict[str, Any]:
        """Convert to Chroma collection metadata format."""
        return {
            "category": self.category.value,
            "description": self.description,
            "tags": ",".join(self.tags),
            "language": self.language,
            "framework": self.framework,
            "version": self.version,
            "hnsw:space": self.distance_metric,
            "hnsw:M": self.hnsw_m,
            "hnsw:construction_ef": self.hnsw_ef_construction,
            "hnsw:search_ef": self.hnsw_ef_search,
        }


# Predefined collection configurations
PREDEFINED_COLLECTIONS: Dict[CollectionCategory, CollectionConfig] = {
    CollectionCategory.PYTHON: CollectionConfig(
        name="python_code",
        category=CollectionCategory.PYTHON,
        description="Python code snippets, libraries, and best practices",
        tags=["python", "code", "programming"],
        language="Python",
    ),
    CollectionCategory.JAVASCRIPT: CollectionConfig(
        name="javascript_code",
        category=CollectionCategory.JAVASCRIPT,
        description="JavaScript/Node.js code and libraries",
        tags=["javascript", "nodejs", "code"],
        language="JavaScript",
    ),
    CollectionCategory.API_DOCS: CollectionConfig(
        name="api_documentation",
        category=CollectionCategory.API_DOCS,
        description="REST API, GraphQL, and other API documentation",
        tags=["api", "documentation", "rest", "graphql"],
    ),
    CollectionCategory.TOOL_DOCS: CollectionConfig(
        name="tool_implementation",
        category=CollectionCategory.TOOL_DOCS,
        description="Tool usage guides, CLI references, and implementation details",
        tags=["tools", "cli", "implementation"],
    ),
    CollectionCategory.FRAMEWORK_DOCS: CollectionConfig(
        name="framework_documentation",
        category=CollectionCategory.FRAMEWORK_DOCS,
        description="Web frameworks, libraries, and SDK documentation",
        tags=["framework", "library", "sdk"],
    ),
    CollectionCategory.ALGORITHMS: CollectionConfig(
        name="algorithms_datastructures",
        category=CollectionCategory.ALGORITHMS,
        description="Algorithms, data structures, and computational theory",
        tags=["algorithms", "data-structures", "theory"],
    ),
    CollectionCategory.SYSTEM_DESIGN: CollectionConfig(
        name="system_design",
        category=CollectionCategory.SYSTEM_DESIGN,
        description="System architecture, design patterns, and scalability",
        tags=["architecture", "design-patterns", "scalability"],
    ),
    CollectionCategory.TUTORIALS: CollectionConfig(
        name="tutorials_guides",
        category=CollectionCategory.TUTORIALS,
        description="Step-by-step tutorials and learning guides",
        tags=["tutorial", "guide", "learning"],
    ),
    CollectionCategory.GENERAL: CollectionConfig(
        name="general_knowledge",
        category=CollectionCategory.GENERAL,
        description="General programming knowledge and miscellaneous content",
        tags=["general", "misc"],
    ),
}


def get_collection_config(category: CollectionCategory) -> CollectionConfig:
    """Get predefined collection configuration."""
    return PREDEFINED_COLLECTIONS.get(category, PREDEFINED_COLLECTIONS[CollectionCategory.GENERAL])


def get_or_create_collection_name(
    category: Optional[CollectionCategory] = None,
    language: Optional[str] = None,
    framework: Optional[str] = None,
) -> str:
    """
    Generate collection name based on category, language, or framework.
    
    Examples:
        - category=PYTHON -> "python_code"
        - language="rust" -> "rust_code"
        - framework="fastapi" -> "framework_documentation"
    """
    if category:
        return category.value
    
    if language:
        lang_lower = language.lower()
        # Check if we have a predefined collection for this language
        for cat, config in PREDEFINED_COLLECTIONS.items():
            if config.language and config.language.lower() == lang_lower:
                return config.name
        # Create new language-specific collection name
        return f"{lang_lower}_code"
    
    if framework:
        return CollectionCategory.FRAMEWORK_DOCS.value
    
    return CollectionCategory.GENERAL.value
