# Tool Catalog

Quick-reference for tools that unlock autonomous agent operation. The orchestrator should consult this before starting any task and proactively suggest relevant tools to the user.

**Principle:** The difference between 5-minute human feedback loops and 25-minute autonomous runs is often a single tool installation.

---

## Top 8 Tools by Autonomy Impact

| Rank | Tool | Impact | Why |
|------|------|--------|-----|
| 1 | **Playwright** | Highest | Visual verification, JS error detection, form testing — eliminates "check the browser" loops |
| 2 | **jq** | High | Parse/validate JSON output without manual inspection — essential for API and config work |
| 3 | **Docker Compose** | High | Spin up full environments (DB, cache, services) — eliminates "I need you to start Postgres" |
| 4 | **curl / httpie** | High | Endpoint testing, API verification — eliminates "can you hit this endpoint?" |
| 5 | **lighthouse** | Medium | Performance/accessibility audits — automated quality gates for web projects |
| 6 | **npm audit / pip-audit** | Medium | Security scanning — catches vulnerabilities before review |
| 7 | **act** | Medium | Run GitHub Actions locally — verify CI without push-and-wait cycles |
| 8 | **sqlite3** | Medium | Quick data inspection/validation — avoids "can you check the DB?" |

---

## Tools by Project Type

| Project Type | Tool Bundle | Install |
|-------------|-------------|---------|
| Node.js web app | Playwright, lighthouse, jq | `npm i -D @playwright/test && npx playwright install` |
| React/Vue/Svelte SPA | Playwright, lighthouse | `npm i -D @playwright/test && npx playwright install` |
| REST API (Node) | httpie, jq | `pip install httpie` (or `brew install httpie jq`) |
| REST API (Python) | httpie, jq | `pip install httpie` |
| Python CLI | pytest (if missing) | `pip install pytest` |
| Python data/ML | pytest, jupyter | `pip install pytest jupyter` |
| Full-stack (DB) | Docker Compose, Playwright, jq | `docker compose up -d` + Playwright install |
| Infrastructure/DevOps | act, docker, jq | `brew install act jq` |

---

## Per-Tool Reference

### Playwright
- **What:** Browser automation and testing framework
- **Install:** `npm i -D @playwright/test && npx playwright install`
- **Suggest when:** Project has visual output (HTML, CSS, UI components)
- **Autonomy unlock:** Verify layouts, catch JS errors, test forms, screenshot comparisons — all without asking the user to open a browser
- **Pitch:** "This is a web project with visual output. If you enable Playwright, I can verify each component visually without asking you to check. Want me to set that up?"

### jq
- **What:** Command-line JSON processor
- **Install:** `brew install jq` / `apt install jq` / `choco install jq`
- **Suggest when:** Project produces or consumes JSON (APIs, configs, data pipelines)
- **Autonomy unlock:** Validate JSON structure, extract fields, diff outputs — without manual inspection

### Docker Compose
- **What:** Multi-container orchestration
- **Install:** Included with Docker Desktop; `docker compose` (v2)
- **Suggest when:** Project needs databases, caches, or external services
- **Autonomy unlock:** Spin up full environments reproducibly — no "start Postgres first" dependencies
- **Pitch:** "This project uses PostgreSQL. If you have Docker, I can spin up the DB automatically with `docker compose up -d`. Want me to create a compose file?"

### curl / httpie
- **What:** HTTP clients for API testing
- **Install:** curl is pre-installed; httpie: `pip install httpie`
- **Suggest when:** Building or modifying API endpoints
- **Autonomy unlock:** Hit endpoints, verify responses, test error cases — all inline

### lighthouse
- **What:** Web performance and accessibility auditor
- **Install:** `npm i -D lighthouse` (or use Chrome DevTools)
- **Suggest when:** Web projects where performance or accessibility matters
- **Autonomy unlock:** Automated performance scores, accessibility violations, SEO checks

### npm audit / pip-audit
- **What:** Dependency vulnerability scanners
- **Install:** Built into npm; `pip install pip-audit`
- **Suggest when:** Any project with third-party dependencies
- **Autonomy unlock:** Catch known vulnerabilities before review phase

### act
- **What:** Run GitHub Actions locally
- **Install:** `brew install act` / `curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash`
- **Suggest when:** Project has `.github/workflows/` and CI matters
- **Autonomy unlock:** Verify CI passes locally without push-and-wait

### sqlite3
- **What:** SQLite command-line interface
- **Install:** Usually pre-installed; `brew install sqlite` if not
- **Suggest when:** Project uses SQLite for local storage
- **Autonomy unlock:** Query data, verify schema, inspect state — no GUI needed

---

## MCP Servers Worth Knowing

These MCP servers provide tool-like capabilities that agents can leverage:

| Server | What It Provides | When to Suggest |
|--------|-----------------|-----------------|
| `@playwright/mcp` | Browser automation via MCP protocol | Web projects — richer than CLI Playwright |
| `context7` | Library documentation lookup | Working with unfamiliar libraries |
| `server-github` | GitHub API access (issues, PRs, repos) | Projects with GitHub integration |
| `server-filesystem` | Sandboxed file operations | When agents need controlled file access |
| `server-memory` | Persistent knowledge graph | Cross-session context preservation |

**Suggesting MCP servers:** Only suggest if the project's `.mcp.json` doesn't already include them. Frame as optional enhancements, not requirements.

---

## How the Orchestrator Uses This

1. **Before starting any task**, identify the project type from package.json / pyproject.toml / file structure
2. **Look up the tool bundle** for that project type
3. **Check which tools are already available** (run `which playwright`, `which jq`, etc.)
4. **Proactively suggest missing tools** that would unlock autonomous runs
5. **Prioritize by autonomy impact** — Playwright for web, jq for APIs, Docker for full-stack
