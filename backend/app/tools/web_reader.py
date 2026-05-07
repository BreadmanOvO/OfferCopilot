import httpx
from bs4 import BeautifulSoup

from app.config import settings


def fetch_page_content(url: str) -> dict[str, str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    try:
        response = httpx.get(url, headers=headers, timeout=settings.fetch_timeout_seconds, follow_redirects=True)
        response.raise_for_status()
    except Exception as e:
        return {"url": url, "title": "", "content": "", "error": str(e)}

    soup = BeautifulSoup(response.text, "lxml")

    title = soup.title.get_text(strip=True) if soup.title else ""

    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    content = soup.get_text(separator="\n", strip=True)
    if len(content) > 8000:
        content = content[:8000]

    return {"url": url, "title": title, "content": content, "error": ""}
