# Deep Research: Graph Databases for Agent Feedback Loops and Knowledge Management

## Context
I'm building several interconnected projects: a multi-agent orchestration system (cc_agents), a personal knowledge base (second-brain), and FPGA tooling projects (tcl_monster, tool-porting). I currently use ChromaDB for vector search/RAG and markdown files for knowledge storage. I suspect graph databases could help with:

1. **Agent feedback loops** — Storing lessons learned from agent runs (what worked, what failed, which constraints prevented bugs) in tcl_monster/tool-porting, then retrieving relevant lessons when similar tasks come up
2. **Knowledge connections** — My second-brain has 14 topic files with cross-cutting connections (an MCP tool might also be relevant to RAG, agents, and dev-tools). Flat files miss these relationships.
3. **Decision tracking** — Architecture decisions have cascading effects across projects. Graph relationships could surface "if you change X, these things are affected."

I want to understand whether graph databases are the right tool here or if I'm overcomplicating things that simpler solutions handle fine.

## What I Need

1. **Graph DB landscape for small/personal use** — What's the right tool for a single developer? Neo4j feels enterprise-heavy. What about embedded/lightweight options (Kuzu, NetworkX, SQLite with recursive CTEs, DGraph)? Comparison of setup complexity, query languages, Python integration.

2. **Graph DB vs vector DB vs both** — When should I use ChromaDB (semantic similarity) vs a graph DB (relationships) vs combining them? Are there hybrid approaches? What does "GraphRAG" actually mean in practice?

3. **Patterns for agent feedback loops** — How are people storing and retrieving lessons learned from AI agent runs? Is a graph DB the right structure, or is a simpler approach (tagged markdown, SQLite) sufficient? What's the query pattern: "I'm about to build X, what lessons from past builds are relevant?"

4. **Knowledge graph for personal knowledge management** — How are developers using graph databases for second-brain/PKM systems? What's the schema? How do you ingest markdown files into a graph? How do you query "show me everything connected to topic X within 2 hops"?

5. **Integration with Claude Code** — Can an agent practically query a graph DB during a build? What's the latency? Is it better as a direct Python recipe (import kuzu) or as an MCP server? Token cost of including graph query results in agent context?

## Output Format

### Key Findings
Numbered list, each with:
- **Finding:** One sentence summary
- **Evidence:** Source/link/example
- **Implication for my projects:** How this affects cc_agents, second-brain, tcl_monster

### Recommended Approach
- What to start with (simplest viable option)
- What to graduate to (if/when scale demands)
- What to skip (overly complex for my use case)

### Constraints & Gotchas
- **Constraint:** What the limitation is
- **Why:** What goes wrong if violated
- **How to verify:** How to test I got it right

### What Others Are Doing
3-5 examples of developers using graph DBs for knowledge management or agent systems, with links.

### Questions I Should Be Asking
Things I didn't think to ask about.

## Scope Boundaries
- Single developer, local-first, Python-based
- Prioritize embedded/lightweight over server-based
- Must work well with Claude Code's Bash/Python execution model
- EE background, comfortable with Python, learning SWE patterns
