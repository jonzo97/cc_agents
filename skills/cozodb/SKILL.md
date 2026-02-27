---
name: cozodb
description: Knowledge graph patterns using CozoDB — GraphRAG retrieval, episodic memory, and markdown ingestion
---

# CozoDB Knowledge Graph Patterns

CozoDB is an embedded graph-relational database with Datalog queries and built-in vector search. It runs locally via SQLite backend — no server needed.

## Install
```bash
pip install pycozo
```

## When to Use CozoDB (vs ChromaDB)

| Need | Use |
|------|-----|
| Pure semantic search over documents | ChromaDB |
| Relationships between entities matter | CozoDB |
| "Show me everything connected to X" queries | CozoDB |
| Agent memory with temporal queries | CozoDB |
| Simple RAG pipeline | ChromaDB |
| Hybrid vector + graph retrieval (GraphRAG) | CozoDB |

## Patterns in This Skill

| Pattern | File | Use Case |
|---------|------|----------|
| **GraphRAG Retrieval** | `graphrag.md` | Vector seed + graph traversal for relationship-aware RAG |
| **Episodic Memory** | `episodic-memory.md` | Agent experience replay: Task > Plan > Action > Observation > Critique |
| **Markdown Ingestion** | `md-ingestion.md` | Incremental pipeline: poll > split > extract > resolve > upsert |

## Shared Gotchas
- Always use `engine='sqlite'` for local persistence — default is in-memory
- CozoScript (Datalog) has a learning curve — test queries in isolation first
- Vector index requires fixed dimensions at creation — match your embedding model
- Entity resolution MUST happen at ingestion time, not query time
- Limit graph traversal to 2-3 hops — dense graphs explode past that
