# CozoDB GraphRAG Retrieval

Hybrid 3-step retrieval: vector seed > graph traverse > serialize to LLM context.

## Quick Patterns

### Setup schema with vector index
```python
from pycozo import Client
db = Client(engine='sqlite', path='./knowledge.db')
db.run(":create node {id: String => type: String, text: String, embedding: <F32; 384>}")
db.run(":create edge {src: String, dst: String => rel: String}")
db.run(":hnsw create node:embedding {dim: 384, dtype: F32, fields: [id, text], ef_construction: 50}")
```

### Step 1: Vector seed — find starting nodes
```python
q_emb = get_embedding("retrieval augmented generation")  # your embedding fn
results = db.run("?[id, text, dist] := ~node:embedding {id, text | "
    f"query: vec({list(q_emb)}), k: 5, bind_distance: dist}}")
seed_ids = [[r[0]] for r in results["rows"][:5]]
```

### Step 2: Graph traversal from seeds (depth-limited)
```python
subgraph = db.run("""
    seed[id] <- $seeds
    reach[s, d, rel, 1] := seed[s], edge{src: s, dst: d, rel}
    reach[s, d, rel, n] := reach[_, s, _, m], edge{src: s, dst: d, rel}, n = m + 1, n <= 3
    ?[src, dst, rel, depth] := reach[src, dst, rel, depth]
""", {"seeds": seed_ids})
```

### Step 3: Serialize sub-graph (token-budgeted)
```python
def serialize_subgraph(rows, max_chars=6000):
    lines, char_count = [], 0
    for src, dst, rel, depth in rows["rows"]:
        line = f"- {src} --[{rel}]--> {dst} (depth {depth})"
        char_count += len(line)
        if char_count > max_chars:
            break
        lines.append(line)
    return "\n".join(lines)
```

## Gotchas
- Limit traversal to 2-3 hops max — dense graphs explode past that
- Token-budget results BEFORE returning to LLM — never dump raw sub-graphs
- Entity resolution at ingestion time, not query time — normalize names on write
- Vector seed should return 2-5 nodes; more seeds = wider but noisier traversal

## When to Use
- RAG where semantic search alone returns structurally wrong results
- "Show me everything connected to X within 2 hops" queries
- Knowledge bases with explicit relationships (not just flat documents)
