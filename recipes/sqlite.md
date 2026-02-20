# SQLite

Local database queries and data inspection. Stdlib, zero install.

## Install
```bash
# Nothing — sqlite3 is Python stdlib
```

## Quick Patterns

### Query and print results
```python
import sqlite3
conn = sqlite3.connect("app.db")
conn.row_factory = sqlite3.Row
rows = conn.execute("SELECT * FROM users WHERE active = 1").fetchall()
for row in rows:
    print(dict(row))
```

### Inspect schema
```python
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
for t in tables:
    cols = conn.execute(f"PRAGMA table_info({t[0]})").fetchall()
    print(f"\n{t[0]}:")
    for c in cols:
        print(f"  {c[1]} ({c[2]})")
```

### Quick data summary
```python
for t in tables:
    count = conn.execute(f"SELECT COUNT(*) FROM {t[0]}").fetchone()[0]
    print(f"  {t[0]}: {count} rows")
```

### Create and populate (for testing)
```python
conn.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, value REAL)")
conn.executemany("INSERT INTO items (name, value) VALUES (?, ?)", [
    ("alpha", 1.0), ("beta", 2.5), ("gamma", 3.7)
])
conn.commit()
```

## Gotchas
- Always `conn.commit()` after writes — SQLite doesn't autocommit by default
- Use `row_factory = sqlite3.Row` for dict-like access instead of tuples
- WAL mode for concurrent reads: `conn.execute("PRAGMA journal_mode=WAL")`

## When to Use
- Inspecting local SQLite databases
- Quick data validation during builds
- Spinning up test databases for integration tests
