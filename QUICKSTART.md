# RAG System - Quick Start Guide

## 🚀 Start the System

### 1. Start Docker Services
```bash
cd docker
docker-compose up -d
```

**Services:**
- Chroma (Vector DB): http://localhost:8000
- Neo4j (Graph DB): http://localhost:7474 (web), bolt://localhost:7687
- Neo4j credentials: neo4j / password

### 2. Start API Server
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate  # Linux/Mac

# Set environment (optional)
$env:LOG_LEVEL = "INFO"
$env:LOG_FORMAT = "colored"  # or "json"
$env:NEO4J_PASSWORD = "password"

# Start server
python -m src.api.main
```

**API will be at**: http://localhost:8080

---

## 📝 CLI Commands

### Document Ingestion

```bash
# Single document
python -m src.cli ingest document myfile.pdf
python -m src.cli ingest document code.py --collection python_code --language python --verbose

# Batch upload
python -m src.cli ingest batch ./documents
python -m src.cli ingest batch ./pdfs --pattern "*.pdf" --collection research --max 100
```

### Query Knowledge Base

```bash
# Simple query
python -m src.cli query "What is machine learning?"

# Query specific collection
python -m src.cli query "Explain decorators" --collection python_code --top-k 10 --verbose
```

### System Management

```bash
# Health check
python -m src.cli health

# List collections
python -m src.cli collections list
```

---

## 🌐 API Endpoints

### Health & Metrics
```bash
# Health check
curl http://localhost:8080/health

# Metrics (JSON)
curl http://localhost:8080/metrics

# Metrics (Prometheus)
curl http://localhost:8080/metrics/prometheus
```

### Document Upload
```bash
# Upload document
curl -X POST http://localhost:8080/upload \
  -F "file=@document.pdf" \
  -F "collection=research"

# Upload with metadata
curl -X POST http://localhost:8080/upload \
  -F "file=@code.py" \
  -F "collection=python_code" \
  -F "language=python"
```

### Query
```bash
# Simple query
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?", "top_k": 5}'

# Query specific collection
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain decorators", "collection": "python_code", "top_k": 10}'
```

### Collections
```bash
# List all collections
curl http://localhost:8080/collections/

# Create collection
curl -X POST http://localhost:8080/collections/create \
  -H "Content-Type: application/json" \
  -d '{"name": "my_docs", "category": "documentation"}'

# Get collection stats
curl http://localhost:8080/collections/my_docs/stats

# Search across collections
curl -X POST http://localhost:8080/collections/search \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "categories": ["documentation", "research"]}'

# Delete collection
curl -X DELETE http://localhost:8080/collections/my_docs
```

### Documents
```bash
# List all documents
curl http://localhost:8080/documents

# Get document details
curl http://localhost:8080/documents/doc_123

# Delete document
curl -X DELETE http://localhost:8080/documents/doc_123
```

---

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Restart a service
docker-compose restart chroma
docker-compose restart neo4j

# Clean up everything (⚠️ deletes data!)
docker-compose down -v
```

---

## 🔍 Troubleshooting

### Chroma Not Connected
```bash
# Check if running
docker ps | grep chroma

# Check logs
docker logs RAG-chroma-1

# Restart
docker-compose restart chroma
```

### Neo4j Not Connected
```bash
# Check if running
docker ps | grep neo4j

# Check logs
docker logs RAG-neo4j-1

# Access web UI
# http://localhost:7474
# Username: neo4j
# Password: password
```

### Python Environment Issues
```bash
# Reinstall dependencies
pip install -e .

# Or install specific packages
pip install typer rich fastapi uvicorn chromadb neo4j graphiti-core
```

### Check System Health
```bash
# Via CLI
python -m src.cli health

# Via API
curl http://localhost:8080/health
```

---

## 📊 Supported File Formats

- **Documents**: PDF, DOCX, TXT, MD, HTML
- **Code**: Python, JavaScript, TypeScript, Java, etc.
- **Size Limit**: 500MB per file
- **Batch**: Up to 100 files at once

---

## 🎯 Collection Categories

**Programming Languages:**
- python_code, javascript_code, typescript_code, java_code, cpp_code, rust_code, go_code

**Documentation:**
- api_documentation, tool_implementation, system_design, algorithms

**Domain Knowledge:**
- research_papers, technical_articles, tutorials, best_practices

**Project Specific:**
- project_docs, meeting_notes, specifications, architecture

**General:**
- general_knowledge, misc

---

## 🔧 Environment Variables

```bash
# Logging
LOG_LEVEL=INFO           # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=colored       # colored or json

# Chroma
CHROMA_HOST=localhost
CHROMA_PORT=8000

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
NEO4J_DATABASE=neo4j

# API
API_HOST=0.0.0.0
API_PORT=8080
```

---

## 📚 Documentation

- **API Docs**: http://localhost:8080/docs (Swagger UI)
- **Redoc**: http://localhost:8080/redoc
- **Health**: http://localhost:8080/health
- **Metrics**: http://localhost:8080/metrics

---

## 🎨 CLI Features

- ✅ Rich progress bars
- ✅ Colored output
- ✅ Tables for results
- ✅ Panels for organization
- ✅ Real-time progress
- ✅ Verbose mode
- ✅ Error messages with context

---

## 🚦 Quick Test

```bash
# 1. Check health
python -m src.cli health

# 2. Upload a document
python -m src.cli ingest document README.md

# 3. Query it
python -m src.cli query "What is this project about?"

# 4. Check API
curl http://localhost:8080/health
```

---

## ✅ Success Criteria

**All should return success:**
- `docker ps` - Shows chroma and neo4j running
- `python -m src.cli health` - All services connected
- `curl http://localhost:8080/health` - Status "healthy"
- Document upload works without errors
- Query returns relevant results

---

## 🆘 Get Help

```bash
# CLI help
python -m src.cli --help
python -m src.cli ingest --help
python -m src.cli query --help

# API docs
# Visit http://localhost:8080/docs
```

---

**Ready to go! 🚀**
