# crawl4ai

LLM-optimized web crawler. Converts pages to clean markdown, handles JS-rendered content, and supports multi-page async crawling.

## Install
```bash
pip install crawl4ai && crawl4ai-setup
```

## Quick Patterns

### Fetch a page as clean markdown
```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://example.com")
        print(result.markdown)  # clean markdown, ready for LLM

asyncio.run(main())
```

### Extract structured data with CSS selectors
```python
from crawl4ai.extraction_strategy import CssExtractionStrategy
import json

schema = {
    "name": "articles",
    "baseSelector": "article.post",
    "fields": [
        {"name": "title", "selector": "h2", "type": "text"},
        {"name": "url", "selector": "a", "type": "attribute", "attribute": "href"},
        {"name": "summary", "selector": "p.excerpt", "type": "text"},
    ],
}

async def main():
    strategy = CssExtractionStrategy(schema)
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://example.com/blog",
            extraction_strategy=strategy,
        )
        data = json.loads(result.extracted_content)

asyncio.run(main())
```

### Crawl with JS execution (SPA/dynamic content)
```python
async def main():
    async with AsyncWebCrawler(browser_type="chromium") as crawler:
        result = await crawler.arun(
            url="https://example.com/app",
            wait_for="css:.content-loaded",
        )
        print(result.markdown)

asyncio.run(main())
```

## Gotchas
- `crawl4ai-setup` installs browser deps (like Playwright) — run it once after pip install
- Default mode is lightweight (no browser). Set `browser_type="chromium"` for JS-heavy pages
- `result.markdown` is the LLM-friendly output; `result.html` has raw HTML if needed
- For large crawls, use `arun_many()` with a list of URLs for async parallelism

## When to Use
- Scraping content to feed into Claude (markdown output is ideal)
- Crawling multiple pages from a site
- JS-rendered pages where you need text, not screenshots
- When you want structured extraction without writing parsing code
