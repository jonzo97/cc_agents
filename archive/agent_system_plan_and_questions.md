# Claude Code Agent System - Plan & Discussion Questions

## Context

I'm an FPGA hardware engineer learning AI concepts and software development through side projects. I want to build a core team of agents to leverage in future projects, moving beyond basic BMAD method to a more sophisticated Scout-Plan-Build system with intelligent context management and research capabilities.

I've been manually running research prompts in Gemini Deep Research, but want a smoother integration. I also need intelligent context management and compaction.

## Research Summary

Based on research into Claude Code 2.0 best practices, multi-agent systems, and current agent orchestration patterns, here's what's working well in 2025:

### Key Findings
- **Lightweight agents** (under 3k tokens) enable fluid orchestration vs heavy agents (25k+) that create bottlenecks
- **Model selection matters**: Haiku for quick tasks, Sonnet for balanced work, Opus for complex reasoning
- **Context engineering is critical**: Auto-compact at 80% threshold, use artifact references instead of copying content
- **Handoff patterns**: Structured handoffs with JSON schemas prevent context loss
- **MCP integration**: Gemini can be integrated via Model Context Protocol servers
- **Checkpointing**: Claude Code 2.0 has built-in checkpoint system for rolling back changes
- **Coordination patterns**: Blackboard (SQLite), hierarchical supervisor, sequential handoffs, parallel execution

### Popular Architectures
1. **Orchestrator-Worker**: Central agent breaks down tasks, delegates to specialists
2. **Sequential Handoff**: Scout → Plan → Build with structured context transfer
3. **Artifact-Centric**: Agents create outputs in external storage, pass lightweight references
4. **Sub-agent with Clean Context**: Specialized agents explore deeply, return condensed summaries

---

## Proposed Agent System Architecture

### Core Agent Team (Phase 1)

#### 1. Scout Agent (Exploration & Discovery)
- **Purpose**: Autonomous codebase exploration, file discovery, dependency analysis
- **Tools**: Read, Glob, Grep, Bash (read-only)
- **Model**: Sonnet (balanced performance)
- **Key Features**:
  - Progressive context discovery
  - Dependency mapping
  - Architecture documentation generation
  - Lightweight context summaries for handoff

#### 2. Research Agent (Deep Analysis)
- **Purpose**: Deep technical research, documentation analysis, best practices discovery
- **Integration**: Gemini Deep Research via MCP server
- **Tools**: WebSearch, WebFetch, Grep, Read
- **Model**: Sonnet with optional Gemini offload
- **Key Features**:
  - Autonomous research workflows
  - Citation tracking
  - Multi-source synthesis
  - Structured research reports

#### 3. Planner Agent (Strategy & Architecture)
- **Purpose**: Analyze scout/research findings, create implementation plans
- **Tools**: Read, TodoWrite, limited Bash
- **Model**: Opus (complex reasoning)
- **Key Features**:
  - Task decomposition
  - Dependency ordering
  - Risk assessment
  - Resource estimation

#### 4. Builder Agent (Implementation)
- **Purpose**: Code implementation based on approved plans
- **Tools**: All file operations (Read, Write, Edit), Bash
- **Model**: Sonnet (balanced)
- **Key Features**:
  - Test-driven development
  - Incremental implementation
  - Checkpoint management
  - Code review integration

#### 5. Context Manager Agent (Background)
- **Purpose**: Monitor context usage, trigger intelligent compaction
- **Tools**: Custom MCP tools for context analysis
- **Model**: Haiku (lightweight, fast)
- **Key Features**:
  - Automatic summarization at 80% threshold
  - Hierarchical note-taking
  - Artifact manifest management
  - Conversation importance scoring

### Supporting Infrastructure (Phase 2)

#### MCP Integrations
- **Gemini Deep Research Server**: For offloading intensive research (exists: ssdeanx/deep-research-mcp-server)
- **SQLite Memory System**: Persistent state, event logging, coordination
- **Artifact Storage**: External storage for large outputs

#### Orchestrator System
- **Pattern**: Hierarchical with handoffs
- **Coordination**: Blackboard pattern via SQLite
- **Handoff Protocol**: Structured JSON summaries
- **Artifact References**: Manifest IDs instead of content copies

#### Context Management System
- **Auto-compaction**: At 80% context threshold
- **Summarization**: Recursive hierarchical
- **Retrieval**: Vector embeddings + just-in-time loading
- **Checkpointing**: Git integration + session state

### Implementation Sequence

#### Stage 1: Foundation (Week 1-2)
1. Create base agent configurations (Scout, Planner, Builder)
2. Set up project structure in `.claude/agents/`
3. Implement basic handoff protocol
4. Test with simple workflows

#### Stage 2: Research Integration (Week 2-3)
1. Set up Gemini MCP server for deep research
2. Create Research Agent configuration
3. Implement research report templates
4. Test research → plan workflow

#### Stage 3: Context Management (Week 3-4)
1. Create Context Manager Agent
2. Implement auto-compaction triggers
3. Set up artifact storage system
4. Build context metrics dashboard

#### Stage 4: Orchestration (Week 4-5)
1. Implement SQLite coordination database
2. Create orchestrator logic
3. Add parallel execution support
4. Implement conflict prevention

#### Stage 5: Polish & Testing (Week 5-6)
1. Build example workflows
2. Create documentation
3. Performance optimization
4. User testing & iteration

### Key Design Principles

1. **Start Simple**: Begin with 3-4 core agents, expand as needed
2. **Lightweight Agents**: Keep prompts under 3k tokens for fluid coordination
3. **Explicit Handoffs**: Use structured transfer_to_XXX functions
4. **Context Efficiency**: Reference artifacts, don't copy
5. **Observable**: Log all handoffs, decisions, and context operations
6. **Recoverable**: Checkpoint before major operations

### Expected Outcomes

- 10x reduction in manual context management
- Autonomous research cycles without manual Gemini queries
- Intelligent agent selection and orchestration
- Persistent memory across sessions
- Scalable to 10+ parallel agents for complex projects

---

## Questions for Discussion

### 1. Immediate Priority
Which agents would be most valuable to you right now?
- Scout (explore codebases)?
- Research (deep technical research)?
- Full Scout-Plan-Build workflow?

### 2. Gemini Setup
Do you have your Gemini API keys ready? Should I prioritize the Gemini Deep Research MCP integration, or start with Claude-only research first?

### 3. Primary Use Cases
What types of projects/tasks will you use this for most?
- FPGA-related tools?
- Learning new frameworks/technologies?
- Building internal team utilities?
- General software development?

### 4. Complexity Preference
Should I:
- **Option A**: Start with a minimal 2-3 agent system and iterate?
- **Option B**: Build the full infrastructure upfront?

### 5. Existing Tools
Are there any specific tools or workflows you're already using that we should integrate with?

### 6. Storage Location
Where should I create this agent system?
- In the current directory (`/home/jorgill/cc_agents`)?
- Should I create a new subdirectory structure?
- Do you want this to be user-level agents (`~/.claude/agents/`) so they're available across all projects, or project-specific?

---

## Additional Considerations to Explore

### Agent Communication Patterns
- Should agents communicate through a central orchestrator, or peer-to-peer?
- How much context should be preserved vs. summarized during handoffs?
- Should there be a "memory agent" that maintains long-term project knowledge?

### Research Workflow
- What triggers a research phase? User request, agent uncertainty, new domain detected?
- How deep should research go? (Gemini Deep Research MCP has 1-5 recursion levels)
- Should research outputs be cached/versioned for reuse?

### Context Management Strategy
- When should compaction happen? (80% threshold, time-based, task-based?)
- What should be preserved vs. summarized? (Recent messages, important decisions, user preferences?)
- Should there be different compaction strategies for different types of work (debugging vs. feature development)?

### Error Handling & Recovery
- What happens if an agent gets stuck or makes a mistake?
- Should there be a "review agent" that validates work before handoff?
- How should the system handle API failures (Gemini, MCP servers)?

### Scalability Concerns
- How many agents should be able to run in parallel?
- Should there be resource limits (API calls, tokens, time)?
- How to prevent agents from stepping on each other's work (file locks, dependency tracking)?

### User Control & Transparency
- How much visibility do you want into agent decisions?
- Should you approve handoffs, or trust the system to orchestrate autonomously?
- What level of logging/tracing is useful vs. overwhelming?

---

## Resources & References

### Key Projects to Learn From
- **wshobson/agents**: 83 production-ready subagents organized by domain
- **Claude Flow**: Enterprise orchestration with SQLite coordination and artifact-centric design
- **deep-research-mcp-server**: Gemini-powered research agent via MCP
- **claude-code-by-agents**: Multi-agent orchestration through @mentions

### Documentation
- [Claude Code Sub-agents Guide](https://docs.claude.com/en/docs/claude-code/sub-agents.md)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [ClaudeLog Agent Engineering](https://claudelog.com/mechanics/agent-engineering/)

### Patterns & Architectures
- Orchestrator-Worker pattern
- Sequential handoff with clean context transfer
- Blackboard coordination (shared state)
- Artifact-centric workflow (reference, don't copy)
- Progressive context discovery
- Just-in-time context loading

---

## Next Steps

After discussing these questions and considerations:
1. Refine the agent architecture based on your specific needs
2. Prioritize which components to build first
3. Begin implementation with a minimal viable system
4. Iterate based on real usage

Feel free to use this document to explore ideas with other AI systems, colleagues, or just for your own planning. Bring back any insights, concerns, or modifications to the plan!