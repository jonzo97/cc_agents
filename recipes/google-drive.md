# Google Drive (via rclone)

Sync files between Google Drive and local directories. Used by the research-liaison agent to pull Gemini Deep Research outputs.

## Install

```bash
sudo apt install rclone  # or: curl https://rclone.org/install.sh | sudo bash

# One-time setup:
rclone config
# Choose: n → name: gdrive → type: drive → client_id: blank → scope: 1 → rest blank → auto config: y
```

## Quick Patterns

### List pending research files
```bash
rclone ls gdrive:"AI Research/pending/"
```

### Pull new files (last 24h)
```bash
rclone copy gdrive:"AI Research/pending/" research/active/ --max-age 24h
```

### Pull a specific file
```bash
rclone copy gdrive:"AI Research/pending/01_output.md" research/active/
```

### Move processed file to ingested
```bash
rclone moveto gdrive:"AI Research/pending/01_output.md" gdrive:"AI Research/ingested/01_output.md"
```

### Export Google Docs as markdown
```bash
rclone copy gdrive:"AI Research/pending/" research/active/ --drive-export-formats md
```

### Diff remote vs local
```bash
rclone check gdrive:"AI Research/pending/" research/active/ --one-way
```

## Gotchas

- **WSL OAuth**: Browser may not open. Install `wslview` (`sudo apt install wslu`) or copy the auth URL and paste token manually.
- **Google Docs ≠ files**: Docs are virtual — rclone exports on download. Use `--drive-export-formats md`. Native `.md` uploads work fine.
- **Rate limits**: Google caps ~10 req/s. Add `--tpslimit 8` for large syncs (50+ files).
- **Shared drives**: Add `--drive-shared-with-me` to see shared files.

## When to Use

- Pulling Gemini Deep Research outputs into the ingestion pipeline
- Syncing research files between Drive and local `research/active/`
- Any file transfer between Google Drive and the local filesystem
