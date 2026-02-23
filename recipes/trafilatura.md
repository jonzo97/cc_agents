# trafilatura

Extract main content from web pages — strips navigation, ads, footers, boilerplate. Best for pulling article text and feeding it to an LLM.

## Install
```bash
pip install trafilatura
```

## Quick Patterns

### Extract article text from a URL
```python
import trafilatura

downloaded = trafilatura.fetch_url("https://example.com/article")
text = trafilatura.extract(downloaded)
print(text)
```

### Extract with metadata (author, date, title)
```python
result = trafilatura.extract(downloaded, output_format="json", with_metadata=True)
# Returns JSON with: title, author, date, text, comments, etc.
```

### Extract as markdown (for LLM consumption)
```python
text = trafilatura.extract(downloaded, output_format="txt", include_links=True)
```

### Batch extract from multiple URLs
```python
import trafilatura
from trafilatura.downloads import fetch_response

urls = ["https://example.com/a", "https://example.com/b"]
for url in urls:
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        text = trafilatura.extract(downloaded)
        print(f"--- {url} ---\n{text}\n")
```

### Extract from raw HTML (already fetched)
```python
text = trafilatura.extract(html_string)
```

## Gotchas
- Returns `None` if it can't find main content — always check the result
- Won't work on JS-rendered pages — pair with Playwright or crawl4ai for those
- `include_links=True` preserves hyperlinks in output — useful for citations
- Handles boilerplate removal automatically (ads, nav, sidebars, footers)
- Has its own fetcher but you can also pass raw HTML from httpx/requests

## When to Use
- Extracting article/blog content for summarization or analysis
- Building a research corpus from web pages
- When you need clean text, not HTML structure
- Preprocessing web content before sending to Claude
- When BeautifulSoup is overkill (you just want the main content, not specific elements)
