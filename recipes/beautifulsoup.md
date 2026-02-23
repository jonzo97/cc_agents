# BeautifulSoup + httpx

Lightweight HTML scraping without a browser. Fast for static pages, structured data extraction, and HTML APIs.

## Install
```bash
pip install beautifulsoup4 httpx lxml
```

## Quick Patterns

### Fetch and parse a page
```python
import httpx
from bs4 import BeautifulSoup

resp = httpx.get("https://example.com", follow_redirects=True, timeout=30)
soup = BeautifulSoup(resp.text, "lxml")
print(soup.title.string)
```

### Extract structured data (table, list, etc.)
```python
rows = []
for tr in soup.select("table tbody tr"):
    cells = [td.get_text(strip=True) for td in tr.select("td")]
    rows.append(cells)
```

### Extract all links
```python
links = [
    {"text": a.get_text(strip=True), "href": a["href"]}
    for a in soup.select("a[href]")
]
```

### Scrape multiple pages
```python
import httpx
from bs4 import BeautifulSoup

with httpx.Client(follow_redirects=True, timeout=30) as client:
    for url in urls:
        resp = client.get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        # extract what you need
```

## Gotchas
- Use `lxml` parser (fast) not `html.parser` (slow, less forgiving)
- Always set `timeout=30` on httpx — default is 5s which is too aggressive
- `follow_redirects=True` is not the default in httpx — you must set it
- For pages that require JS rendering, this won't work — use Playwright instead
- Respect `robots.txt` and rate-limit with `time.sleep()` between requests

## When to Use
- Static pages or server-rendered HTML (no JS needed to load content)
- Extracting structured data (tables, lists, product listings)
- Scraping multiple pages quickly without browser overhead
- When Playwright is overkill (no JS, no screenshots, no interaction needed)
