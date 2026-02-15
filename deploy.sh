#!/bin/bash
# Deploy agents from cc_agents to ~/.claude/agents/
#
# Usage:
#   ./deploy.sh                # Deploy base agents
#   ./deploy.sh --serena       # Deploy Serena-enhanced variants (scout, builder, reviewer)
#   ./deploy.sh --clean        # Remove agents from target not in source
#   ./deploy.sh --dry-run      # Preview without changes
#   ./deploy.sh --serena --dry-run  # Preview Serena deployment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_SRC="$SCRIPT_DIR/agents"
SERENA_SRC="$SCRIPT_DIR/agents/serena"
AGENTS_DST="$HOME/.claude/agents"

DRY_RUN=false
CLEAN=false
SERENA=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --clean)   CLEAN=true ;;
        --serena)  SERENA=true ;;
        *)         echo "Unknown option: $arg"; exit 1 ;;
    esac
done

[ "$DRY_RUN" = true ] && echo "[DRY RUN] No files will be modified."

echo "=== cc_agents deploy ==="
echo "Source: $AGENTS_SRC"
[ "$SERENA" = true ] && echo "Serena: $SERENA_SRC (overrides for scout, builder, reviewer)"
echo "Target: $AGENTS_DST"
echo ""

# Backup current agents
if [ "$DRY_RUN" = false ]; then
    BACKUP_DIR="$AGENTS_DST/.backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    cp "$AGENTS_DST"/*.md "$BACKUP_DIR/" 2>/dev/null || true
    echo "Backed up current agents to: $BACKUP_DIR"
    echo ""
fi

# Deploy base agents
echo "--- Base agents ---"
for agent_file in "$AGENTS_SRC"/*.md; do
    agent_name=$(basename "$agent_file")
    lines=$(wc -l < "$agent_file")

    if [ "$DRY_RUN" = true ]; then
        if diff -q "$agent_file" "$AGENTS_DST/$agent_name" >/dev/null 2>&1; then
            echo "  $agent_name ($lines lines) — unchanged"
        else
            echo "  $agent_name ($lines lines) — CHANGED"
        fi
    else
        cp "$agent_file" "$AGENTS_DST/$agent_name"
        echo "  Deployed: $agent_name ($lines lines)"
    fi
done

# Deploy Serena variants (overwrite base versions for scout, builder, reviewer)
if [ "$SERENA" = true ] && [ -d "$SERENA_SRC" ]; then
    echo ""
    echo "--- Serena variants (overriding base) ---"
    for agent_file in "$SERENA_SRC"/*.md; do
        agent_name=$(basename "$agent_file")
        lines=$(wc -l < "$agent_file")

        if [ "$DRY_RUN" = true ]; then
            echo "  $agent_name ($lines lines) — Serena override"
        else
            cp "$agent_file" "$AGENTS_DST/$agent_name"
            echo "  Deployed: $agent_name ($lines lines) [Serena]"
        fi
    done
fi

# Clean: remove stale agents
echo ""
if [ "$CLEAN" = true ]; then
    echo "--- Cleaning stale agents ---"
    for target_file in "$AGENTS_DST"/*.md; do
        target_name=$(basename "$target_file")
        if [ ! -f "$AGENTS_SRC/$target_name" ]; then
            if [ "$DRY_RUN" = true ]; then
                echo "  Would remove: $target_name (not in source)"
            else
                read -p "  Remove $target_name? [y/N] " confirm
                if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
                    rm "$target_file"
                    echo "  Removed: $target_name"
                else
                    echo "  Kept: $target_name"
                fi
            fi
        fi
    done
else
    echo "--- Stale agents (not in source, use --clean to remove) ---"
    found_stale=false
    for target_file in "$AGENTS_DST"/*.md; do
        target_name=$(basename "$target_file")
        if [ ! -f "$AGENTS_SRC/$target_name" ]; then
            echo "  $target_name"
            found_stale=true
        fi
    done
    [ "$found_stale" = false ] && echo "  (none)"
fi

echo ""
echo "Done. Restart Claude Code to pick up changes."
