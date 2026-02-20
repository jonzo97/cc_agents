# JSON Processing (Python)

Parse, filter, and transform JSON without jq dependency. Use Python's stdlib for anything an agent would use jq for.

## Install
```bash
# Nothing — json is stdlib
```

## Quick Patterns

### Parse and filter JSON file
```python
import json
data = json.load(open("data.json"))
filtered = [item for item in data if item["status"] == "active"]
print(json.dumps(filtered, indent=2))
```

### Extract nested fields
```python
names = [item["user"]["name"] for item in data if "user" in item]
```

### Validate JSON structure
```python
import json, sys
try:
    data = json.load(open(sys.argv[1]))
    print(f"Valid JSON: {type(data).__name__}, {len(data) if hasattr(data, '__len__') else 'scalar'}")
except json.JSONDecodeError as e:
    print(f"Invalid JSON at line {e.lineno}: {e.msg}")
```

### Diff two JSON files
```python
import json
a = json.load(open("before.json"))
b = json.load(open("after.json"))
# For simple diffs:
added = set(b.keys()) - set(a.keys()) if isinstance(a, dict) else None
print(f"Added keys: {added}")
```

### Pretty-print from CLI
```bash
python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin),indent=2))" < data.json
```

## Gotchas
- `json.loads()` for strings, `json.load()` for files — easy to mix up
- Large files: use `ijson` for streaming (`pip install ijson`)

## When to Use
- Any project that produces or consumes JSON (APIs, configs, data pipelines)
- Validating API responses, config files, or build outputs
