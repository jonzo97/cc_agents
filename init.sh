#!/bin/bash
# Initialize a project with cc_agents experimental agents
#
# Usage:
#   ./init.sh <project-path>                  # Copy base agents
#   ./init.sh <project-path> --serena         # Copy Serena-enhanced variants
#   ./init.sh <project-path> --dry-run        # Preview what would be copied
#   ./init.sh <project-path> --serena --dry-run
#   ./init.sh <project-path> --remove         # Remove cc_agents from project
#
# Examples:
#   ./init.sh ~/some-new-project
#   ./init.sh ~/some-new-project --serena
#   ./init.sh /mnt/c/tcl_monster --dry-run
#   ./init.sh ~/fpga_mcp --remove

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_SRC="$SCRIPT_DIR/agents"
SERENA_SRC="$SCRIPT_DIR/agents/serena"

# --- Argument parsing ---

if [ -z "$1" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage: ./init.sh <project-path> [options]"
    echo ""
    echo "Copies experimental agents from cc_agents into a project's .claude/agents/"
    echo "directory. Project-level agents override the vanilla globals in ~/.claude/agents/."
    echo ""
    echo "Options:"
    echo "  --serena    Use Serena-enhanced variants for scout, builder, reviewer"
    echo "  --dry-run   Preview what would be copied without making changes"
    echo "  --remove    Remove cc_agents agents from project (revert to vanilla globals)"
    echo ""
    echo "Examples:"
    echo "  ./init.sh ~/some-new-project"
    echo "  ./init.sh ~/some-new-project --serena"
    echo "  ./init.sh /mnt/c/tcl_monster --dry-run"
    echo "  ./init.sh ~/fpga_mcp --remove"
    exit 0
fi

PROJECT_PATH="$1"
shift

MODE="init"
SERENA=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) MODE="dry-run" ;;
        --remove)  MODE="remove" ;;
        --serena)  SERENA=true ;;
        *)         echo "Unknown option: $arg"; exit 1 ;;
    esac
done

# --- Validation ---

if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Project directory not found: $PROJECT_PATH"
    exit 1
fi

PROJECT_NAME=$(basename "$PROJECT_PATH")
AGENTS_DST="$PROJECT_PATH/.claude/agents"

echo "=== cc_agents init ==="
echo "Project:  $PROJECT_NAME ($PROJECT_PATH)"
echo "Source:   $AGENTS_SRC"
[ "$SERENA" = true ] && echo "Serena:   $SERENA_SRC (overrides for scout, builder, reviewer)"
echo "Target:   $AGENTS_DST"
echo "Mode:     $MODE"
echo ""

# --- Remove mode ---

if [ "$MODE" = "remove" ]; then
    if [ ! -d "$AGENTS_DST" ]; then
        echo "No .claude/agents/ directory found. Nothing to remove."
        exit 0
    fi

    echo "Removing cc_agents from $PROJECT_NAME..."
    echo "These agents will be removed (project will fall back to vanilla globals):"
    for f in "$AGENTS_DST"/*.md; do
        [ -f "$f" ] && echo "  - $(basename "$f")"
    done

    read -p "Proceed? [y/N] " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        # Only remove agents that exist in cc_agents source (don't touch project-specific agents)
        for agent_file in "$AGENTS_SRC"/*.md; do
            agent_name=$(basename "$agent_file")
            if [ -f "$AGENTS_DST/$agent_name" ]; then
                rm "$AGENTS_DST/$agent_name"
                echo "  Removed: $agent_name"
            fi
        done
        # Remove agents dir if empty
        rmdir "$AGENTS_DST" 2>/dev/null && echo "  Removed empty agents/ directory" || true
        echo ""
        echo "Done. $PROJECT_NAME will now use vanilla agents from ~/.claude/agents/"
    else
        echo "Cancelled."
    fi
    exit 0
fi

# --- Init / Dry-run mode ---

# Check for existing project agents
if [ -d "$AGENTS_DST" ] && [ "$(ls -A "$AGENTS_DST"/*.md 2>/dev/null)" ]; then
    echo "Note: Project already has agents in .claude/agents/:"
    for f in "$AGENTS_DST"/*.md; do
        [ -f "$f" ] && echo "  - $(basename "$f")"
    done
    echo ""
    echo "Existing agents will be overwritten if they have the same name."
    echo "Project-specific agents (not in cc_agents) will be preserved."
    echo ""
fi

if [ "$MODE" = "dry-run" ]; then
    echo "[DRY RUN] Would copy these agents:"
    for agent_file in "$AGENTS_SRC"/*.md; do
        agent_name=$(basename "$agent_file")
        lines=$(wc -l < "$agent_file")
        if [ -f "$AGENTS_DST/$agent_name" ]; then
            echo "  $agent_name ($lines lines) — overwrite existing"
        else
            echo "  $agent_name ($lines lines) — new"
        fi
    done
    if [ "$SERENA" = true ] && [ -d "$SERENA_SRC" ]; then
        echo ""
        echo "Serena overrides:"
        for agent_file in "$SERENA_SRC"/*.md; do
            agent_name=$(basename "$agent_file")
            lines=$(wc -l < "$agent_file")
            echo "  $agent_name ($lines lines) — Serena variant"
        done
    fi
    echo ""
    echo "[DRY RUN] No files were modified."
    exit 0
fi

# Create target directory
mkdir -p "$AGENTS_DST"

# Copy base agents
echo "Copying agents..."
for agent_file in "$AGENTS_SRC"/*.md; do
    agent_name=$(basename "$agent_file")
    lines=$(wc -l < "$agent_file")
    cp "$agent_file" "$AGENTS_DST/$agent_name"
    echo "  $agent_name ($lines lines)"
done

# Overwrite with Serena variants if requested
if [ "$SERENA" = true ] && [ -d "$SERENA_SRC" ]; then
    echo ""
    echo "Applying Serena overrides..."
    for agent_file in "$SERENA_SRC"/*.md; do
        agent_name=$(basename "$agent_file")
        lines=$(wc -l < "$agent_file")
        cp "$agent_file" "$AGENTS_DST/$agent_name"
        echo "  $agent_name ($lines lines) [Serena]"
    done
fi

echo ""
echo "=== Done ==="
echo ""
echo "Experimental agents installed in $PROJECT_NAME."
echo "These override the vanilla agents in ~/.claude/agents/."
echo ""
echo "To revert to vanilla: ./init.sh $PROJECT_PATH --remove"
echo "To update agents:     edit agents/*.md in cc_agents, then re-run init.sh"
