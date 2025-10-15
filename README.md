# Universal File-to-Knowledge Converter

Transform any file (PDF, DOCX, TXT, MD, HTML, MP3) into LLM-ready knowledge with automatic embeddings and knowledge graph generation.

## Features

- **Multi-Format Support**: Process PDF, DOCX, TXT, MD, HTML, and MP3 (audio transcription)
- **Vector Search**: Semantic search using Chroma vector database with HNSW indexes
- **Knowledge Graph**: Automatic entity and relationship extraction with Neo4j
- **Hybrid Search**: Combine vector similarity with graph traversals using RRF
- **Batch Processing**: Process multiple documents in parallel with progress tracking
- **Streaming Responses**: Real-time progress updates for long-running operations
- **Docker-First**: Complete orchestration with Chroma, Neo4j, API, and Worker containers

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- OpenAI or Anthropic API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd RAG
```

2. Configure environment:
```bash
cp docker/.env.example docker/.env
# Edit docker/.env with your API keys
```

3. Start services:
```bash
cd docker
docker-compose up -d
```

4. Verify services are healthy:
```bash
docker-compose ps
```

### Usage

#### Upload a Document
```bash
curl -X POST http://localhost:8080/api/v1/ingest/document \
  -H "X-API-Key: your-api-key" \
  -F "file=@document.pdf"
```

#### Query Knowledge Base
```bash
curl -X POST http://localhost:8080/api/v1/query \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the main topic?", "mode": "hybrid"}'
```

#### Batch Upload
```bash
curl -X POST http://localhost:8080/api/v1/ingest/batch \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"directory": "/path/to/documents"}'
```

## Development

### Local Setup

1. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

4. Code quality checks:
```bash
ruff check src/
mypy src/
```

### Project Structure

```
src/
├── models/          # Pydantic models (Document, Chunk, Embedding, Entity, etc.)
├── ingestion/       # Document processing pipeline
├── storage/         # Database clients (Chroma, Neo4j)
├── retrieval/       # Search logic (vector, graph, hybrid)
├── agent/           # Conversational AI agent
├── api/             # FastAPI endpoints
├── cli/             # Command-line interface
└── config/          # Configuration management

tests/
├── unit/            # Unit tests for models and utilities
├── integration/     # Integration tests with databases
└── contract/        # Contract tests for MCP servers

docker/
├── docker-compose.yml  # Service orchestration
├── Dockerfile.api      # FastAPI container
├── Dockerfile.worker   # Background worker container
└── .env.example        # Environment template
```

## Architecture

### Services

1. **Chroma**: Vector database for embeddings (port 8000)
2. **Neo4j**: Knowledge graph database (ports 7474, 7687)
3. **API**: FastAPI server for REST endpoints (port 8080)
4. **Worker**: Background processor for document ingestion

### Data Flow

1. Document upload → Docling extraction → Text chunks
2. Chunks → OpenAI/Anthropic embeddings → Chroma storage
3. Chunks → Graphiti entity extraction → Neo4j knowledge graph
4. Query → Vector search + Graph traversal → RRF fusion → Results

## Performance

- **Response Time**: <500ms cached, <2s vector search, <5s graph traversal
- **Memory**: <2GB per container (8GB total for 4 containers)
- **Throughput**: 100+ documents/minute batch processing
- **Concurrency**: 10+ simultaneous users supported

## Constitution Compliance

This project follows strict development principles:

- **Pydantic-First**: All data models use Pydantic validation
- **MCP Integration**: Leverages Context7, DeepWiki, GitHub MCP servers
- **TDD**: Tests written before implementation
- **Streaming UX**: Long operations provide real-time progress
- **Performance-First**: Optimized for <2s response times

## License

MIT License - See LICENSE file for details

## Contributing

See CONTRIBUTING.md for development guidelines.
