# DigitalOcean Deployment Complete Guide

## ✅ Local Docker Cleanup - COMPLETED

### What Was Removed:
- ✅ **4 containers** (qdrant-agentkit, qdrant-mcp-server, codegraph-mcp-server, neo4j-codegraph)
- ✅ **9 volumes** (all data volumes for Neo4j, Chroma, etc.)
- ✅ **2 custom networks** (rag_default, codegraph_mcp_codegraph-network)
- ✅ **All Docker images** (Qdrant, Neo4j, ChromaDB, MCP servers)
- ✅ **16.46 GB** of disk space reclaimed

### Current Local Docker State:
```
Containers: 0
Volumes: 0
Images: 0
Networks: 0 (only default Docker networks remain)
```

**Your local Docker is now completely clean!** ✨

---

## 🌊 DigitalOcean Droplet Information

### Droplet Details:
```
IP Address (IPv4): 165.232.174.154
Private IP: 10.104.0.2
Region: (Your selected region)
Password: 837829318aA!a
Status: Running
```

### What You'll Deploy:
1. **Qdrant** - Vector database (ports 6333, 6334)
2. **PostgreSQL + pgvector** - Relational DB with vector search (port 5432)
3. **Neo4j** - Knowledge graph database (ports 7687, 7474)

---

## 🚀 Deployment Steps

### Step 1: Connect to Your Droplet

**From Windows PowerShell:**
```powershell
ssh root@165.232.174.154
# Password when prompted: 837829318aA!a
```

**First login tips:**
- Answer "yes" to fingerprint prompt
- You'll see: `Welcome to Ubuntu...`
- You're now on the cloud server!

---

### Step 2: Run the Deployment Script

**Copy and paste this entire block into your droplet SSH session:**

```bash
# Download and run deployment script
curl -fsSL https://raw.githubusercontent.com/eldon31/processorAI/main/scripts/deploy_to_digitalocean.sh -o setup.sh

# Make it executable
chmod +x setup.sh

# Run the setup
./setup.sh
```

**OR manually paste the script:**

If the above doesn't work, I've created `scripts/deploy_to_digitalocean.sh` in your repo. You can:

1. Copy the entire script content
2. SSH into your droplet
3. Run: `nano setup.sh`
4. Paste the script
5. Press `Ctrl+X`, then `Y`, then `Enter`
6. Run: `chmod +x setup.sh && ./setup.sh`

---

### Step 3: What the Script Does

The deployment script will:

1. ✅ **Update system packages**
2. ✅ **Install Docker & Docker Compose**
3. ✅ **Create project directory** (`/opt/rag-system`)
4. ✅ **Generate docker-compose.yml** with all services
5. ✅ **Configure firewall** (UFW) to allow necessary ports
6. ✅ **Start all services** (Qdrant, PostgreSQL, Neo4j)
7. ✅ **Show connection information**

**Expected duration:** 5-10 minutes

---

### Step 4: Verify Deployment

**After the script completes, you should see:**

```
======================================
   SETUP COMPLETE!
=======================================

🌐 Connection Information:

Qdrant:
  HTTP:  http://165.232.174.154:6333
  gRPC:  165.232.174.154:6334
  Dashboard: http://165.232.174.154:6333/dashboard

PostgreSQL:
  Host: 165.232.174.154
  Port: 5432
  Database: rag_db
  User: rag_user
  Password: 837829318aA!a

Neo4j:
  Bolt: bolt://165.232.174.154:7687
  Browser: http://165.232.174.154:7474
  User: neo4j
  Password: 837829318aA!a
```

---

## 🧪 Test Connections from Your Windows Machine

### Option A: Run PowerShell Test Script

**From your RAG project directory:**
```powershell
.\scripts\test_cloud_connections.ps1
```

This will test all connections and show you what's accessible.

---

### Option B: Manual Testing

#### Test Qdrant:
```python
from qdrant_client import QdrantClient

client = QdrantClient(
    host="165.232.174.154",
    port=6333,
    timeout=30
)

# Should return empty list (no collections yet)
print(client.get_collections())
```

#### Test Qdrant Dashboard:
Open in browser: `http://165.232.174.154:6333/dashboard`

#### Test PostgreSQL:
```python
import psycopg2

conn = psycopg2.connect(
    host="165.232.174.154",
    port=5432,
    database="rag_db",
    user="rag_user",
    password="837829318aA!a"
)

print("PostgreSQL connected!")
conn.close()
```

#### Test Neo4j:
Open in browser: `http://165.232.174.154:7474`
- Username: `neo4j`
- Password: `837829318aA!a`

---

## 📝 Update Your Code to Use Cloud Services

### Before (Local):
```python
# Old local connections
qdrant_client = QdrantClient(host="localhost", port=6333)
neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
```

### After (Cloud):
```python
# New cloud connections
qdrant_client = QdrantClient(
    host="165.232.174.154",  # Your droplet IP
    port=6333,
    timeout=60
)

neo4j_driver = GraphDatabase.driver(
    "bolt://165.232.174.154:7687",
    auth=("neo4j", "837829318aA!a")
)
```

---

## 🔐 Security Considerations

### Current Setup (Development):
- ✅ Firewall enabled (UFW)
- ⚠️ Services are publicly accessible (development mode)
- ⚠️ No HTTPS (HTTP only)
- ⚠️ Password in plain text (acceptable for dev/testing)

### For Production (Future):
1. **Enable HTTPS** with Let's Encrypt/Caddy
2. **Use environment variables** for passwords
3. **Restrict IP access** (only allow your IP)
4. **Enable Qdrant API keys**
5. **Use managed databases** (DigitalOcean Managed PostgreSQL)

---

## 💰 Cost Breakdown

### Current Setup:
- **Droplet:** ~$12-24/month (depending on size)
- **Storage:** Included in droplet price
- **Bandwidth:** 1TB/month included
- **Total:** ~$12-24/month

### Optimization Tips:
- Use DigitalOcean Spaces for backups ($5/month, 250GB)
- Enable automatic backups ($2.40-4.80/month, 20% of droplet cost)
- Use managed databases for production (starts at $15/month)

---

## 🛠️ Useful Commands (On Droplet)

### View all services:
```bash
cd /opt/rag-system
docker-compose ps
```

### View logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f qdrant
docker-compose logs -f postgres
docker-compose logs -f neo4j
```

### Restart services:
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart qdrant
```

### Stop all services:
```bash
docker-compose down
```

### Start all services:
```bash
docker-compose up -d
```

### Check disk usage:
```bash
df -h
docker system df
```

---

## 📦 Upload Kaggle Embeddings to Cloud Qdrant

After processing embeddings on Kaggle, upload them to your cloud Qdrant:

### Update `scripts/upload_to_qdrant.py`:

```python
# Change this line:
client = QdrantClient(host="localhost", port=6333)

# To this:
client = QdrantClient(host="165.232.174.154", port=6333, timeout=120)
```

### Then upload:
```powershell
# Upload each collection
python scripts/upload_to_qdrant.py `
    --collection viator_api `
    --file path/to/viator_api_embeddings.jsonl `
    --mode upsert

python scripts/upload_to_qdrant.py `
    --collection fast_docs `
    --file path/to/fast_docs_embeddings.jsonl `
    --mode upsert

# ... etc for other collections
```

---

## 🔄 Backup and Restore

### Backup Qdrant Data:
```bash
# On droplet
cd /opt/rag-system
docker exec qdrant tar -czf /tmp/qdrant_backup.tar.gz /qdrant/storage
docker cp qdrant:/tmp/qdrant_backup.tar.gz ./backups/qdrant_$(date +%Y%m%d).tar.gz
```

### Backup PostgreSQL:
```bash
docker exec postgres-rag pg_dump -U rag_user rag_db > backup_$(date +%Y%m%d).sql
```

### Backup Neo4j:
```bash
docker exec neo4j-rag neo4j-admin database dump neo4j > neo4j_backup_$(date +%Y%m%d).dump
```

---

## 🚨 Troubleshooting

### Can't connect to Qdrant?
```bash
# Check if service is running
docker-compose ps

# Check Qdrant logs
docker-compose logs qdrant

# Check firewall
sudo ufw status
```

### Out of disk space?
```bash
# Check usage
df -h

# Clean Docker
docker system prune -af --volumes
```

### Services won't start?
```bash
# Check logs
docker-compose logs

# Restart Docker daemon
systemctl restart docker

# Recreate containers
docker-compose down
docker-compose up -d --force-recreate
```

---

## 📊 Monitoring

### Check service health:
```bash
# All containers
docker-compose ps

# Qdrant health
curl http://localhost:6333/health

# PostgreSQL health
docker exec postgres-rag pg_isready -U rag_user

# Neo4j health
docker exec neo4j-rag cypher-shell -u neo4j -p 837829318aA!a "RETURN 1"
```

---

## 🎯 Next Steps

### Immediate (After Deployment):
1. ✅ SSH into droplet and run deployment script
2. ✅ Test connections from Windows using test script
3. ✅ Open Qdrant dashboard in browser
4. ✅ Verify all services are running

### Short-term (This Week):
1. 📊 Process embeddings on Kaggle
2. ⬆️ Upload embeddings to cloud Qdrant
3. 🔗 Update agentic-rag to use cloud services
4. 🧪 Test Phase 1 integration

### Long-term (Production):
1. 🔒 Enable HTTPS with Caddy
2. 🔑 Set up API keys and authentication
3. 📈 Set up monitoring (Grafana + Prometheus)
4. 💾 Automate backups with cron
5. 🌍 Add custom domain name

---

## 📞 Support

### DigitalOcean Resources:
- Documentation: https://docs.digitalocean.com/
- Community: https://www.digitalocean.com/community
- Support: Available through dashboard

### Docker Commands Cheat Sheet:
```bash
docker ps                    # List running containers
docker logs <container>      # View container logs
docker exec -it <container> bash  # Enter container
docker-compose restart       # Restart all services
docker system df             # Check disk usage
```

---

## ✅ Summary

### What You've Done:
- ✅ Cleaned up local Docker (16.46GB freed)
- ✅ Prepared deployment scripts for DigitalOcean
- ✅ Ready to deploy Qdrant, PostgreSQL, Neo4j to cloud

### What's Next:
1. **SSH into droplet** → Run deployment script
2. **Test connections** → Verify all services work
3. **Process on Kaggle** → Generate embeddings
4. **Upload to cloud** → Populate Qdrant
5. **Integrate agent** → Phase 1 implementation

**You're ready to go cloud! 🚀**
