# ChromaDB

Embedding database for RAG, semantic search, and knowledge bases. Runs locally, no server needed.

## Install
```bash
pip install chromadb
```

## Quick Patterns

### Create a collection and add documents
```python
import chromadb
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("my_docs")
collection.add(
    documents=["First document text", "Second document text"],
    ids=["doc1", "doc2"],
    metadatas=[{"source": "file1.md"}, {"source": "file2.md"}]
)
```

### Semantic search
```python
results = collection.query(query_texts=["what is the architecture?"], n_results=5)
for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
    print(f"[{dist:.3f}] {meta['source']}: {doc[:100]}")
```

### Filter by metadata
```python
results = collection.query(
    query_texts=["deployment"],
    n_results=5,
    where={"source": {"$eq": "README.md"}}
)
```

### Bulk ingest from files
```python
import glob, os
files = glob.glob("docs/**/*.md", recursive=True)
collection.add(
    documents=[open(f).read() for f in files],
    ids=[os.path.relpath(f) for f in files],
    metadatas=[{"source": os.path.relpath(f)} for f in files]
)
```

## Gotchas
- `PersistentClient` saves to disk; `Client()` is ephemeral (lost on exit)
- Default embedding model is `all-MiniLM-L6-v2` — good enough for most cases, no API key needed
- IDs must be unique; re-adding same ID silently overwrites — use `upsert()` if intentional
- Distances are L2 by default; lower = more similar. Use `hnsw:space: cosine` for cosine similarity

## When to Use
- Building RAG over local documents
- Semantic search across a codebase, notes, or knowledge base
- Any time you'd reach for a vector DB but don't want server overhead
