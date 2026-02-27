# CozoDB Markdown Ingestion

Incremental pipeline: poll > split > extract > resolve > upsert to knowledge graph.

## Quick Patterns

### Setup schema
```python
from pycozo import Client
import os, glob, re, time, hashlib
db = Client(engine='sqlite', path='./kb.db')
db.run(":create doc {path: String => hash: String, updated_at: Float}")
db.run(":create chunk {id: String => doc_path: String, heading: String, text: String}")
db.run(":create entity {name: String => type: String, source_chunk: String}")
```

### Poll for modified files (incremental — skip unchanged)
```python
def get_modified(doc_dir, db):
    modified = []
    for path in glob.glob(f"{doc_dir}/**/*.md", recursive=True):
        content = open(path).read()
        file_hash = hashlib.md5(content.encode()).hexdigest()
        existing = db.run("?[hash] := doc{path: $p, hash}", {"p": path})
        if not existing["rows"] or existing["rows"][0][0] != file_hash:
            modified.append((path, content, file_hash))
    return modified
```

### Split on headers + upsert chunks
```python
def ingest_file(path, content, file_hash, db):
    sections = re.split(r'^(#{1,2} .+)$', content, flags=re.MULTILINE)
    heading, chunks = "intro", []
    for s in sections:
        if re.match(r'^#{1,2} ', s): heading = s.strip('# ').strip()
        elif s.strip(): chunks.append([f"{path}::{heading}", path, heading, s.strip()])
    db.run("?[id,d,h,t] <- $data :put chunk {id=>doc_path:d,heading:h,text:t}", {"data":chunks})
    db.run("?[p,h,ts] <- [[$p,$h,$ts]] :put doc {path:p => hash:h, updated_at:ts}",
           {"p": path, "h": file_hash, "ts": time.time()})
```

### Entity resolution (normalize before write — prevents duplicate nodes)
```python
CANONICAL = {"xilinx vivado": "vivado", "intel quartus": "quartus"}
def normalize(name): return CANONICAL.get(name.lower().strip(), name.lower().strip())
```

## Gotchas
- Only reprocess modified docs — full re-index is O(n) LLM calls, incremental is O(changed)
- Entity resolution MUST happen at ingestion — "Vivado" vs "Xilinx Vivado" = duplicates
- Schema drift is inevitable with LLM extraction — enforce a fixed ontology of types
- Use content hash (not mtime) to detect changes — mtime is unreliable across systems

## When to Use
- Building a knowledge graph from markdown notes or a second brain
- Incremental indexing where full re-ingestion is too expensive
