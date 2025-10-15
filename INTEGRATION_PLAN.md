# Integration Plan: Agentic RAG Knowledge Graph + Qdrant Collections

## 🎯 Executive Summary

We have **two powerful systems** that can be integrated to create an enterprise-grade agentic RAG platform:

### System 1: Agentic RAG Knowledge Graph (PostgreSQL + Neo4j)
- ✅ **Complete AI Agent Framework** (Pydantic AI)
- ✅ **Knowledge Graph** (Neo4j + Graphiti) for temporal relationships
- ✅ **Vector Search** (PostgreSQL + pgvector)
- ✅ **Streaming FastAPI** with real-time responses
- ✅ **CLI Interface** with tool usage visibility
- ⚠️ **Limitation:** Small dataset (21 big tech docs), OpenAI embeddings (1536-dim)

### System 2: Qdrant Collections (Production-Ready)
- ✅ **4 Large Collections** (~19,000+ chunks total)
  - `viator_api`: 995 chunks (API documentation)
  - `fast_docs`: ~3,000 chunks (FastAPI/FastMCP/Python SDK)
  - `pydantic_docs`: ~7,000 chunks (Pydantic library)
  - `inngest_ecosystem`: ~8,000 chunks (Inngest workflows)
- ✅ **Code-Optimized Embeddings** (nomic-embed-code, 768-dim)
- ✅ **Qdrant Vector DB** (fast, scalable, production-ready)
- ⚠️ **Limitation:** No agent framework, basic search only

---

## 🚀 Integration Strategy: 3-Phase Approach

### **PHASE 1: Quick Win - Add Qdrant to Existing Agent** ⭐ RECOMMENDED START
**Goal:** Keep everything in agentic-rag, just add Qdrant as additional data source  
**Effort:** Low (1-2 days)  
**Value:** Immediate access to 19K+ technical docs through agent

#### What We'll Do:
1. **Add Qdrant client** to `agent/db_utils.py`
2. **Create new tool** `qdrant_search_tool` in `agent/tools.py`
3. **Register with agent** in `agent/agent.py`
4. **Keep existing PostgreSQL + Neo4j** for big tech docs
5. **Agent decides** when to use Qdrant vs PostgreSQL vs Neo4j

#### Architecture After Phase 1:
```
┌─────────────────────────────────────────────────────────────┐
│                    Pydantic AI Agent                         │
│  (Decides which data source based on query intent)          │
└────────┬────────────────────────┬───────────────┬───────────┘
         │                        │               │
    ┌────▼─────┐          ┌──────▼──────┐  ┌────▼─────┐
    │PostgreSQL│          │    Neo4j    │  │  Qdrant  │  ← NEW!
    │ pgvector │          │  Knowledge  │  │ 4 Large  │
    │Big Tech  │          │    Graph    │  │Collections│
    │21 docs   │          │ Temporal    │  │ 19K docs │
    └──────────┘          └─────────────┘  └──────────┘
```

#### Code Changes Required:

**1. Install Qdrant client:**
```bash
pip install qdrant-client
```

**2. Add to `agent/db_utils.py`:**
```python
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue

# Initialize Qdrant client
qdrant_client = QdrantClient(host="localhost", port=6333)

async def qdrant_search(
    collection_name: str,
    query_vector: List[float],
    limit: int = 10,
    score_threshold: float = 0.5
) -> List[Dict[str, Any]]:
    """Search Qdrant collection with vector similarity."""
    try:
        results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold
        )
        
        return [
            {
                "id": hit.id,
                "score": hit.score,
                "content": hit.payload.get("text", ""),
                "metadata": hit.payload.get("metadata", {}),
                "collection": collection_name
            }
            for hit in results
        ]
    except Exception as e:
        logger.error(f"Qdrant search error: {e}")
        return []
```

**3. Add to `agent/tools.py`:**
```python
class QdrantSearchInput(BaseModel):
    """Input for Qdrant search across technical documentation."""
    query: str = Field(..., description="Search query")
    collections: List[str] = Field(
        default=["viator_api", "fast_docs", "pydantic_docs", "inngest_ecosystem"],
        description="Collections to search (default: all)"
    )
    limit: int = Field(default=10, description="Results per collection")

async def qdrant_search_tool(input_data: QdrantSearchInput) -> List[Dict[str, Any]]:
    """
    Search technical documentation in Qdrant.
    
    Collections available:
    - viator_api: Viator Partner API documentation
    - fast_docs: FastAPI, FastMCP, Python SDK
    - pydantic_docs: Pydantic library documentation
    - inngest_ecosystem: Inngest workflow platform
    
    Returns:
        Combined results from all requested collections
    """
    # Generate embedding using nomic-embed-code
    embedding = await generate_code_embedding(input_data.query)
    
    all_results = []
    for collection in input_data.collections:
        results = await qdrant_search(
            collection_name=collection,
            query_vector=embedding,
            limit=input_data.limit
        )
        all_results.extend(results)
    
    # Sort by score
    all_results.sort(key=lambda x: x["score"], reverse=True)
    
    return all_results[:input_data.limit * len(input_data.collections)]
```

**4. Register tool in `agent/agent.py`:**
```python
@rag_agent.tool
async def search_technical_docs(
    ctx: RunContext[AgentDependencies],
    query: str,
    collections: List[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Search technical documentation (APIs, frameworks, libraries).
    
    Use this tool when users ask about:
    - Viator API, travel APIs
    - FastAPI, FastMCP, Python SDKs
    - Pydantic models, validation
    - Inngest workflows, background jobs
    
    Args:
        query: Technical question or keyword
        collections: Specific collections to search (default: all)
        limit: Maximum results per collection
    
    Returns:
        Relevant technical documentation chunks
    """
    input_data = QdrantSearchInput(
        query=query,
        collections=collections or ["viator_api", "fast_docs", "pydantic_docs", "inngest_ecosystem"],
        limit=limit
    )
    
    return await qdrant_search_tool(input_data)
```

**5. Update system prompt in `agent/prompts.py`:**
```python
SYSTEM_PROMPT = """You are an expert AI assistant with access to multiple knowledge sources:

1. **Big Tech & AI Strategy** (PostgreSQL + Knowledge Graph):
   - Investment trends, funding rounds
   - Company strategies, executive moves
   - Temporal relationships and timelines
   
2. **Technical Documentation** (Qdrant):
   - Viator API: Travel/tours API integration
   - FastAPI/FastMCP: Web frameworks and MCP servers
   - Pydantic: Data validation and models
   - Inngest: Workflow automation and background jobs

TOOL SELECTION GUIDELINES:
- For business/strategy questions → Use PostgreSQL + Neo4j
- For technical/code questions → Use Qdrant search
- For comprehensive answers → Combine both sources

Always cite your sources and indicate which knowledge base you used.
"""
```

#### Benefits:
✅ **Minimal code changes** (~200 lines)  
✅ **No data migration** needed  
✅ **Keep all existing features** (knowledge graph, streaming, CLI)  
✅ **Immediate value** - access to 19K+ technical docs  
✅ **Agent intelligently routes** queries to right data source  

---

### **PHASE 2: Advanced Integration - Unified Search**
**Goal:** Create hybrid search that combines PostgreSQL, Neo4j, and Qdrant  
**Effort:** Medium (3-5 days)  
**Value:** Best-of-all-worlds search experience

#### What We'll Add:
1. **Unified search orchestrator** that queries all sources
2. **Result merging** with score normalization
3. **Deduplication** across sources
4. **Relevance re-ranking** using cross-encoder
5. **Collection-aware routing** (auto-detect which collections to query)

#### New Tool:
```python
@rag_agent.tool
async def unified_search(
    ctx: RunContext[AgentDependencies],
    query: str,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Search across ALL knowledge sources and combine results.
    
    This tool automatically:
    1. Detects query intent (business vs technical)
    2. Queries relevant sources in parallel
    3. Merges and ranks results
    4. Returns top N most relevant
    
    Use this for complex queries that might span multiple domains.
    """
    # Parallel search across all sources
    pgvector_task = vector_search_tool(query, limit)
    neo4j_task = graph_search_tool(query)
    qdrant_task = qdrant_search_tool(query, collections=["all"])
    
    results = await asyncio.gather(pgvector_task, neo4j_task, qdrant_task)
    
    # Normalize scores and merge
    merged = normalize_and_merge(results)
    
    # Re-rank with cross-encoder
    reranked = await rerank_results(query, merged)
    
    return reranked[:limit]
```

---

### **PHASE 3: Migration & Consolidation** 
**Goal:** Migrate big tech docs to Qdrant, sunset PostgreSQL pgvector  
**Effort:** Medium (2-3 days)  
**Value:** Simplified architecture, single vector DB

#### Migration Steps:

1. **Create new Qdrant collection:**
```python
qdrant_client.create_collection(
    collection_name="big_tech_ai",
    vectors_config={
        "size": 768,  # Switch to nomic-embed-code
        "distance": "Cosine"
    }
)
```

2. **Re-embed big tech docs** with nomic-embed-code:
```bash
python scripts/migrate_to_qdrant.py \
    --source postgres \
    --target qdrant \
    --collection big_tech_ai
```

3. **Update agent tools** to use Qdrant for everything
4. **Keep Neo4j** for knowledge graph (temporal relationships)
5. **Remove PostgreSQL pgvector dependency**

#### Final Architecture:
```
┌─────────────────────────────────────────────────────────┐
│                  Pydantic AI Agent                       │
└────────┬───────────────────────────┬────────────────────┘
         │                           │
    ┌────▼─────────┐          ┌─────▼──────┐
    │    Qdrant    │          │   Neo4j    │
    │ Vector Search│          │  Knowledge │
    │              │          │   Graph    │
    │ Collections: │          │  Temporal  │
    │ - viator_api │          │Relationships│
    │ - fast_docs  │          └────────────┘
    │ - pydantic   │
    │ - inngest    │
    │ - big_tech ← │ NEW!
    └──────────────┘
```

---

## 🎬 Recommended Action Plan

### Week 1: Phase 1 Implementation
**Days 1-2: Setup**
- [ ] Add `qdrant-client` to requirements.txt
- [ ] Create `agent/qdrant_utils.py` with connection utilities
- [ ] Add Qdrant search function to `agent/db_utils.py`

**Days 3-4: Tool Integration**
- [ ] Create `qdrant_search_tool` in `agent/tools.py`
- [ ] Register tool with agent in `agent/agent.py`
- [ ] Update system prompt with Qdrant collections info
- [ ] Add code embedding support (nomic-embed-code)

**Day 5: Testing & Refinement**
- [ ] Test queries across all collections
- [ ] Verify agent tool selection logic
- [ ] Test CLI with technical queries
- [ ] Benchmark search performance

### Week 2: Phase 2 (Optional)
**Days 1-3: Unified Search**
- [ ] Implement result merging logic
- [ ] Add score normalization
- [ ] Create reranking pipeline
- [ ] Test hybrid search quality

**Days 4-5: Optimization**
- [ ] Add caching layer
- [ ] Optimize parallel queries
- [ ] Performance tuning
- [ ] Documentation

### Future: Phase 3 (Optional)
- Only if PostgreSQL pgvector becomes a bottleneck
- Or if you want to consolidate to single vector DB

---

## 📊 Comparison: Before vs After

| Feature | Before | After Phase 1 | After Phase 3 |
|---------|--------|---------------|---------------|
| **Vector DB** | PostgreSQL pgvector | PostgreSQL + Qdrant | Qdrant only |
| **Knowledge Graph** | Neo4j | Neo4j | Neo4j |
| **Total Documents** | 21 | 19,021 | 19,021 |
| **Data Sources** | 1 (big tech) | 5 (big tech + 4 collections) | 5 collections |
| **Embedding Model** | OpenAI (1536d) | OpenAI + nomic-code (768d) | nomic-code (768d) |
| **Agent Tools** | 7 | 8 | 7 |
| **Search Speed** | Fast | Fast | Faster |
| **Infrastructure** | PostgreSQL + Neo4j | PostgreSQL + Neo4j + Qdrant | Qdrant + Neo4j |

---

## 🔧 Technical Considerations

### Embedding Model Strategy
**Current State:**
- **Big tech docs:** OpenAI text-embedding-3-small (1536-dim)
- **Qdrant collections:** nomic-embed-code (768-dim)

**Phase 1 Approach:**
- Keep both embeddings
- Generate query embedding based on target collection
- Agent auto-detects which embedding to use

**Phase 3 Approach:**
- Re-embed everything with nomic-embed-code
- Single embedding model = simpler architecture
- Better for code/technical content

### Cost Considerations
- **OpenAI embeddings:** $0.020 / 1M tokens
- **Nomic embeddings:** Free (local) or $0.001 / 1M tokens (API)
- **Phase 3 migration:** One-time re-embedding cost (~21 docs × $0.020)

### Performance Impact
- **Qdrant:** ~10-50ms per query (depends on collection size)
- **PostgreSQL pgvector:** ~20-100ms per query
- **Neo4j graph traversal:** ~50-200ms per query
- **Parallel queries:** No performance penalty (run concurrently)

---

## 🎯 Success Metrics

### Phase 1 Goals:
- ✅ Agent can answer technical questions (FastAPI, Pydantic, Inngest, Viator)
- ✅ Search across 19,000+ chunks
- ✅ Tool selection accuracy >90%
- ✅ Response time <2 seconds

### Phase 2 Goals:
- ✅ Unified search combines all sources
- ✅ Result quality improvement (measured by user feedback)
- ✅ Deduplication rate >95%

### Phase 3 Goals:
- ✅ Single vector DB (Qdrant)
- ✅ Reduced infrastructure complexity
- ✅ Faster query performance

---

## 💡 Alternative Approaches

### Option A: Separate Agents (Microservices)
- **Agentic RAG Agent:** Handles big tech/business queries
- **Technical Docs Agent:** Handles code/API queries  
- **Router Agent:** Decides which agent to invoke

**Pros:** Clean separation, independent scaling  
**Cons:** More complex architecture, higher latency

### Option B: Migrate Everything to Qdrant (Skip Phase 1)
- Re-embed all docs immediately
- Use only Qdrant + Neo4j

**Pros:** Simpler final state  
**Cons:** No quick win, higher upfront effort

### Option C: Keep Systems Separate
- Use agentic-rag for business queries
- Use Qdrant directly for technical queries
- No integration

**Pros:** Zero effort  
**Cons:** No unified interface, duplicate tooling

---

## 📝 Next Steps

**RECOMMENDED: Start with Phase 1**

1. **Today:** Review this plan, decide on Phase 1 approach
2. **Tomorrow:** Set up development environment, install qdrant-client
3. **Day 3-4:** Implement Qdrant integration (follow code examples above)
4. **Day 5:** Test and validate with real queries
5. **Week 2:** Decide if Phase 2/3 needed based on Phase 1 results

**Questions to Answer:**
- Which embedding model for big tech docs? (Keep OpenAI or switch to nomic?)
- Do we need unified search (Phase 2) or is separate tools enough?
- Timeline for full migration (Phase 3)?

**I'm ready to help implement any phase! Just let me know which approach you prefer.** 🚀
