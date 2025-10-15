#!/bin/bash
# DigitalOcean Droplet Setup Script
# Run this on your droplet: ssh root@165.232.174.154
# Password: 837829318aA!a

set -e  # Exit on error

echo "======================================="
echo "   DIGITALOCEAN DROPLET SETUP"
echo "======================================="

# Update system
echo ""
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# Install Docker if not already installed
echo ""
echo "🐳 Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    echo "✓ Docker installed"
else
    echo "✓ Docker already installed"
fi

# Install Docker Compose
echo ""
echo "📦 Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    apt install -y docker-compose
    echo "✓ Docker Compose installed"
else
    echo "✓ Docker Compose already installed"
fi

# Create project directory
echo ""
echo "📁 Creating project directory..."
mkdir -p /opt/rag-system
cd /opt/rag-system

# Create docker-compose.yml
echo ""
echo "📝 Creating docker-compose.yml..."
cat > docker-compose.yml <<'EOF'
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_storage:/qdrant/storage
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: ankane/pgvector:latest
    container_name: postgres-rag
    environment:
      POSTGRES_USER: rag_user
      POSTGRES_PASSWORD: 837829318aA!a
      POSTGRES_DB: rag_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U rag_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  neo4j:
    image: neo4j:latest
    container_name: neo4j-rag
    environment:
      NEO4J_AUTH: neo4j/837829318aA!a
      NEO4J_PLUGINS: '["apoc", "graph-data-science"]'
      NEO4J_dbms_security_procedures_unrestricted: apoc.*,gds.*
    ports:
      - "7687:7687"  # Bolt
      - "7474:7474"  # HTTP
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "837829318aA!a", "RETURN 1"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  qdrant_storage:
    driver: local
  postgres_data:
    driver: local
  neo4j_data:
    driver: local
  neo4j_logs:
    driver: local

networks:
  default:
    name: rag-network
EOF

echo "✓ docker-compose.yml created"

# Configure firewall
echo ""
echo "🔥 Configuring firewall..."
ufw --force enable
ufw allow 22/tcp      # SSH
ufw allow 6333/tcp    # Qdrant HTTP
ufw allow 6334/tcp    # Qdrant gRPC
ufw allow 5432/tcp    # PostgreSQL
ufw allow 7687/tcp    # Neo4j Bolt
ufw allow 7474/tcp    # Neo4j HTTP
ufw reload
echo "✓ Firewall configured"

# Start services
echo ""
echo "🚀 Starting all services..."
docker-compose up -d

# Wait for services to be healthy
echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose ps

# Show connection info
echo ""
echo "======================================="
echo "   SETUP COMPLETE!"
echo "======================================="
echo ""
echo "🌐 Connection Information:"
echo ""
echo "Qdrant:"
echo "  HTTP:  http://165.232.174.154:6333"
echo "  gRPC:  165.232.174.154:6334"
echo "  Dashboard: http://165.232.174.154:6333/dashboard"
echo ""
echo "PostgreSQL:"
echo "  Host: 165.232.174.154"
echo "  Port: 5432"
echo "  Database: rag_db"
echo "  User: rag_user"
echo "  Password: 837829318aA!a"
echo ""
echo "Neo4j:"
echo "  Bolt: bolt://165.232.174.154:7687"
echo "  Browser: http://165.232.174.154:7474"
echo "  User: neo4j"
echo "  Password: 837829318aA!a"
echo ""
echo "======================================="
echo ""
echo "📝 Next Steps:"
echo "1. Test connections from your local machine"
echo "2. Upload Kaggle embeddings to cloud Qdrant"
echo "3. Configure agentic-rag to use cloud services"
echo ""
echo "🔧 Useful Commands:"
echo "  docker-compose logs -f          # View logs"
echo "  docker-compose ps               # Check status"
echo "  docker-compose restart          # Restart all"
echo "  docker-compose down             # Stop all"
echo ""
