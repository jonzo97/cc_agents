---
feature: "[name]"
status: draft  # draft | approved | in-progress | completed
files_modified:
  - path/to/file.py
  - path/to/other.py
must_haves:
  truths:
    - "User can [do X] via [entry point]"          # behavioral — verified end-to-end
  artifacts:
    - path: "src/module.py"
      contains: "def function_name"                 # grep-verifiable
  wired:
    - from: "src/module.py"
      to: "src/dependency.py"
      pattern: "import.*dependency"                 # grep-verifiable
---

## Objective

[1-2 sentences: what this plan achieves and why]

## Tasks

### 1. [Task title] — [Now] ~Nmin
- **Files:** `path/to/file.py`
- **Action:** [What to change/create]
- **Constraints (from research):** [Hard limits, gotchas, anti-patterns]
- **Verify:** [How to confirm this task is done — test command, grep, etc.]
- **Done when:** [Acceptance criterion]

### 2. [Task title] — [Next ~5min]
- **Files:** `path/to/other.py`
- **Action:** [What to change/create]
- **Constraints (from research):** [Hard limits, gotchas, anti-patterns]
- **Verify:** [How to confirm this task is done]
- **Done when:** [Acceptance criterion]

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [risk] | low/med/high | low/med/high | [how to handle] |

## Checkpoints

- After task N: [what to verify end-to-end]
