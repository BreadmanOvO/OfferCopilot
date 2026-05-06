from typing import Any

import httpx
from bs4 import BeautifulSoup

from app.config import settings


def generate_search_queries(company: str, intent: dict[str, Any], jd_text: str = "") -> list[str]:
    city = intent.get("city", "")
    role = intent.get("target_role") or intent.get("role", "")

    queries = [
        f"{company} company overview",
        f"{company} careers jobs",
        f"{company} recruitment",
    ]

    if city:
        queries.append(f"{company} {city}")
    if role:
        queries.append(f"{company} {role}")

    return queries


def search_ddg(query: str) -> list[dict[str, str]]:
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    try:
        response = httpx.post(url, data={"q": query}, headers=headers, timeout=settings.fetch_timeout_seconds, follow_redirects=True)
        response.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(response.text, "lxml")
    results = []

    for link in soup.select(".result__a")[:settings.search_max_results]:
        title = link.get_text(strip=True)
        href = link.get("href", "")
        snippet_el = link.find_parent(".result") or link.find_parent("div")
        snippet = ""
        if snippet_el:
            snippet_tag = snippet_el.select_one(".result__snippet")
            if snippet_tag:
                snippet = snippet_tag.get_text(strip=True)

        if title and href:
            results.append({"title": title, "url": href, "snippet": snippet})

    return results
