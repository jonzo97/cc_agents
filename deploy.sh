#!/bin/bash
# Deploy modernized agents from cc_agents to ~/.claude/agents/
# Usage: ./deploy.sh [--dry-run]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_SRC="$SCRIPT_DIR/agents"
AGENTS_DST="$HOME/.claude/agents"

DRY_RUN=false
if [ "$1" = "--dry-run" ]; then
    DRY_RUN=true
    echo "[DRY RUN] No files will be modified."
fi

echo "=== cc_agents deploy ==="
echo "Source: $AGENTS_SRC"
echo "Target: $AGENTS_DST"
echo ""

# Backup current agents
if [ "$DRY_RUN" = false ]; then
    BACKUP_DIR="$AGENTS_DST/.backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    cp "$AGENTS_DST"/*.md "$BACKUP_DIR/" 2>/dev/null || true
    echo "Backed up current agents to: $BACKUP_DIR"
fi

# Deploy each agent
for agent_file in "$AGENTS_SRC"/*.md; do
    agent_name=$(basename "$agent_file")
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would copy: $agent_name"
        diff "$agent_file" "$AGENTS_DST/$agent_name" 2>/dev/null && echo "  (no changes)" || echo "  (changed)"
    else
        cp "$agent_file" "$AGENTS_DST/$agent_name"
        echo "Deployed: $agent_name"
    fi
done

echo ""

# Report what's in target but not in source (stale agents)
echo "=== Stale agents in ~/.claude/agents/ (not in cc_agents) ==="
for target_file in "$AGENTS_DST"/*.md; do
    target_name=$(basename "$target_file")
    if [ ! -f "$AGENTS_SRC/$target_name" ]; then
        echo "  $target_name (consider removing)"
    fi
done

echo ""
echo "Done. Restart Claude Code to pick up changes."
