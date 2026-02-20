# HTTP Requests

API testing and endpoint verification. Use Python requests (no extra deps on most systems) or curl.

## Install
```bash
pip install requests  # usually already available
```

## Quick Patterns

### GET with response validation
```python
import requests
r = requests.get("http://localhost:8000/api/users")
assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text[:200]}"
data = r.json()
print(f"Got {len(data)} users")
```

### POST with JSON body
```python
r = requests.post("http://localhost:8000/api/users", json={
    "name": "Test User",
    "email": "test@example.com"
})
assert r.status_code == 201, f"Create failed: {r.text[:200]}"
```

### Auth headers
```python
headers = {"Authorization": f"Bearer {token}"}
r = requests.get("http://localhost:8000/api/me", headers=headers)
```

### Quick smoke test (curl, no Python needed)
```bash
curl -s http://localhost:8000/health | python3 -c "import json,sys; d=json.load(sys.stdin); print('OK' if d.get('status')=='ok' else f'FAIL: {d}')"
```

### Test multiple endpoints
```python
endpoints = ["/health", "/api/users", "/api/config"]
for ep in endpoints:
    r = requests.get(f"http://localhost:8000{ep}")
    status = "OK" if r.ok else "FAIL"
    print(f"  {status} {ep} [{r.status_code}]")
```

## Gotchas
- `r.json()` throws if response isn't JSON — check `Content-Type` or wrap in try/except
- Timeout defaults to None (waits forever) — always pass `timeout=10`
- For file uploads: `requests.post(url, files={"file": open("f.txt", "rb")})`

## When to Use
- Building or modifying API endpoints
- Smoke testing a running server
- Verifying webhook payloads or auth flows
