from playwright.sync_api import sync_playwright


def fetch_page_with_browser(url: str) -> dict[str, str]:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            title = page.title()
            content = page.inner_text("body")
            browser.close()

            if len(content) > 8000:
                content = content[:8000]

            return {"url": url, "title": title, "content": content, "error": ""}
    except Exception as e:
        return {"url": url, "title": "", "content": "", "error": str(e)}
