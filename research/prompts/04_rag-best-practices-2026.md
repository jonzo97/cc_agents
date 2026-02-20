# Deep Research: RAG Best Practices in 2026

## Context
I'm building RAG pipelines for personal knowledge management and developer tooling. I currently use ChromaDB for vector storage with default embeddings (all-MiniLM-L6-v2). My use cases: searching project documentation, retrieving relevant lessons from past agent runs, and building a queryable knowledge base from bookmarks and notes. I want to make sure I'm not using 2024 patterns when better approaches exist.

## What I Need

1. **Embedding model landscape Feb 2026** — What's the current best embedding model for code + technical documentation? Is all-MiniLM-L6-v2 still reasonable or significantly outdated? What about Nomic, Jina, BGE, or Anthropic's own embeddings? Trade-offs between quality, speed, and local vs API.

2. **Chunking strategies that actually matter** — Semantic chunking vs fixed-size vs recursive. What does the evidence say about which approach produces better retrieval? For mixed content (code + prose + tables), what works best? What chunk sizes are people using in 2026?

3. **Hybrid search (vector + keyword)** — BM25 + vector search combination. Is this standard practice now? What ratio/fusion approach works best? How to implement with ChromaDB or alternatives?

4. **Reranking** — Cross-encoder reranking after initial retrieval. Is this worth the complexity for small collections (<10K documents)? What reranker models work locally? Cohere reranker vs local alternatives.

5. **GraphRAG and structured retrieval** — Microsoft's GraphRAG approach. Is it practical for small-scale use? How does it compare to plain vector RAG for my use cases? When is it overkill vs genuinely helpful?

6. **Evaluation** — How do I know if my RAG pipeline is working well? What metrics matter? RAGAS, manual evaluation, A/B testing approaches for a solo developer.

## Output Format

### Key Findings
Numbered list, each with:
- **Finding:** One sentence summary
- **Evidence:** Source/link/benchmark
- **Implication for my setup:** What I should change or keep

### Recommended Stack
For my specific use case (small collection, local-first, Python, code + docs):
- Embedding model: [recommendation]
- Chunking strategy: [recommendation]
- Search approach: [recommendation]
- Reranking: [yes/no and what]
- Evaluation: [how to measure]

### Constraints & Gotchas
- Common mistakes in RAG implementations
- Things that seem like improvements but aren't worth it at small scale
- Embedding model compatibility issues

### What Others Are Doing
3-5 practical RAG implementations from developers (not enterprise), with links.

### Questions I Should Be Asking

## Scope Boundaries
- Small scale: <10K documents, single user
- Local-first: must run without API keys ideally
- Python-based, must work with Claude Code's Bash execution
- Prioritize retrieval quality over speed (not serving production traffic)
