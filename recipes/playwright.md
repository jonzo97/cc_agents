# Playwright

Browser automation for visual verification, testing, and scraping. The #1 tool for autonomous web project work.

## Install
```bash
pip install playwright && playwright install chromium
```

## Quick Patterns

### Screenshot a page
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:3000")
    page.screenshot(path="screenshot.png", full_page=True)
    browser.close()
```

### Check for JS errors
```python
errors = []
page.on("pageerror", lambda e: errors.append(str(e)))
page.goto(url)
page.wait_for_load_state("networkidle")
if errors:
    print(f"JS ERRORS: {errors}")
```

### Assert visible text
```python
from playwright.sync_api import expect
expect(page.locator("h1")).to_have_text("Welcome")
expect(page.locator(".error")).not_to_be_visible()
```

### Fill and submit a form
```python
page.fill("#email", "test@example.com")
page.fill("#password", "testpass123")
page.click("button[type=submit]")
page.wait_for_url("**/dashboard")
```

## Gotchas
- Always `wait_for_load_state("networkidle")` before screenshots — otherwise you get half-rendered pages
- `chromium` is fastest to install; use it unless you specifically need Firefox/WebKit
- Headless by default; use `launch(headless=False)` for debugging
- For SPAs, `wait_for_selector(".loaded-indicator")` is more reliable than networkidle

## When to Use
- Web project with visual output (HTML, CSS, UI components)
- Need to verify forms, navigation, or interactive elements
- Want to catch JS errors without opening a browser manually
