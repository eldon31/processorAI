# Test Connection to DigitalOcean Services
# Run this from your Windows machine after deployment

Write-Host "`n=======================================" -ForegroundColor Cyan
Write-Host "   TESTING DIGITALOCEAN CONNECTIONS   " -ForegroundColor Yellow
Write-Host "=======================================" -ForegroundColor Cyan

$DROPLET_IP = "165.232.174.154"
$PASSWORD = "837829318aA!a"

# Test 1: Qdrant
Write-Host "`n🔍 Testing Qdrant..." -ForegroundColor Yellow
try {
    python -c "from qdrant_client import QdrantClient; c = QdrantClient(host='$DROPLET_IP', port=6333, timeout=10); print('✓ Qdrant connection successful!'); print(f'  Collections: {len(c.get_collections().collections)}')"
    Write-Host "✓ Qdrant is accessible" -ForegroundColor Green
} catch {
    Write-Host "✗ Qdrant connection failed" -ForegroundColor Red
    Write-Host "  Error: $_" -ForegroundColor Gray
}

# Test 2: Qdrant Dashboard
Write-Host "`n🌐 Testing Qdrant Dashboard..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://${DROPLET_IP}:6333/dashboard" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Qdrant Dashboard accessible at: http://${DROPLET_IP}:6333/dashboard" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Dashboard connection failed" -ForegroundColor Red
}

# Test 3: PostgreSQL
Write-Host "`n🗄️  Testing PostgreSQL..." -ForegroundColor Yellow
try {
    python -c "import psycopg2; conn = psycopg2.connect(host='$DROPLET_IP', port=5432, database='rag_db', user='rag_user', password='$PASSWORD', connect_timeout=10); print('✓ PostgreSQL connection successful!'); conn.close()"
    Write-Host "✓ PostgreSQL is accessible" -ForegroundColor Green
} catch {
    Write-Host "⚠ PostgreSQL test skipped (psycopg2 not installed)" -ForegroundColor Yellow
    Write-Host "  Install: pip install psycopg2-binary" -ForegroundColor Gray
}

# Test 4: Neo4j
Write-Host "`n📊 Testing Neo4j..." -ForegroundColor Yellow
try {
    python -c "from neo4j import GraphDatabase; driver = GraphDatabase.driver('bolt://$DROPLET_IP:7687', auth=('neo4j', '$PASSWORD')); driver.verify_connectivity(); print('✓ Neo4j connection successful!'); driver.close()"
    Write-Host "✓ Neo4j is accessible" -ForegroundColor Green
    Write-Host "  Browser: http://${DROPLET_IP}:7474" -ForegroundColor Cyan
} catch {
    Write-Host "⚠ Neo4j test skipped (neo4j driver not installed)" -ForegroundColor Yellow
    Write-Host "  Install: pip install neo4j" -ForegroundColor Gray
}

# Summary
Write-Host "`n=======================================" -ForegroundColor Cyan
Write-Host "   CONNECTION TEST COMPLETE   " -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Cyan

Write-Host "`n📝 Connection Details:" -ForegroundColor Yellow
Write-Host "  Droplet IP: $DROPLET_IP" -ForegroundColor White
Write-Host "  Password: $PASSWORD" -ForegroundColor White

Write-Host "`n🔗 Quick Access URLs:" -ForegroundColor Yellow
Write-Host "  Qdrant Dashboard: http://${DROPLET_IP}:6333/dashboard" -ForegroundColor Cyan
Write-Host "  Neo4j Browser: http://${DROPLET_IP}:7474" -ForegroundColor Cyan

Write-Host "`n💡 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Update your Python scripts to use cloud endpoints" -ForegroundColor White
Write-Host "  2. Upload Kaggle embeddings to cloud Qdrant" -ForegroundColor White
Write-Host "  3. Configure agentic-rag to connect to cloud services" -ForegroundColor White

Write-Host "`n=======================================" -ForegroundColor Cyan
