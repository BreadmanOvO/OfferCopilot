from __future__ import annotations

import logging
import re
from typing import Any
from urllib.parse import quote_plus

import httpx
from bs4 import BeautifulSoup

from app.config import settings
from app.tools.llm_client import llm

logger = logging.getLogger(__name__)

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def generate_search_queries(company: str, intent: dict[str, Any], jd_text: str = "") -> list[str]:
    """Generate search queries for a company.

    Uses LLM when configured for smarter, context-aware queries.
    Falls back to template-based queries.
    """
    if llm.is_configured:
        try:
            return _llm_queries(company, intent, jd_text)
        except Exception as e:
            logger.warning("LLM query generation failed, falling back to templates: %s", e)

    return _template_queries(company, intent, jd_text)


def _llm_queries(company: str, intent: dict[str, Any], jd_text: str = "") -> list[str]:
    city = intent.get("city", "")
    role = intent.get("target_role") or intent.get("role", "")
    field = intent.get("technical_field", "")

    context_parts = [f"公司: {company}"]
    if field:
        context_parts.append(f"技术方向: {field}")
    if role:
        context_parts.append(f"目标职位: {role}")
    if city:
        context_parts.append(f"城市: {city}")
    if jd_text:
        context_parts.append(f"JD关键词: {jd_text[:200]}")

    messages = [
        {
            "role": "system",
            "content": (
                "你是一个搜索专家。根据公司和职位信息，生成5条最有效的搜索查询。\n"
                "查询应该覆盖：公司概况、招聘信息、技术栈、薪资待遇、员工评价。\n"
                "优先使用中文查询（除非公司是外企）。\n"
                '返回JSON格式: {"queries": ["query1", "query2", ...]}\n'
                "只返回JSON。"
            ),
        },
        {"role": "user", "content": "\n".join(context_parts)},
    ]

    result = llm.chat_json(messages, max_tokens=512, temperature=0.5)
    queries = result.get("queries", [])

    if not queries:
        raise RuntimeError("LLM returned empty query list")

    return queries[:5]


def _template_queries(company: str, intent: dict[str, Any], jd_text: str = "") -> list[str]:
    city = intent.get("city", "")
    role = intent.get("target_role") or intent.get("role", "")

    queries = [
        f"{company} 公司概况",
        f"{company} 招聘",
        f"{company} 怎么样",
    ]

    if city:
        queries.append(f"{company} {city}")
    if role:
        queries.append(f"{company} {role}")

    return queries


def search(query: str) -> list[dict[str, str]]:
    """Search using available engines with fallback.

    Priority: Sogou -> Google -> DuckDuckGo
    """
    for engine in [_search_sogou, _search_google, _search_ddg]:
        try:
            results = engine(query)
            if results:
                return results
        except Exception as e:
            logger.debug("Search engine %s failed: %s", engine.__name__, e)
    return []


def _search_sogou(query: str) -> list[dict[str, str]]:
    """Search via Sogou (搜狗) — best for Chinese queries."""
    url = f"https://www.sogou.com/web?query={quote_plus(query)}"
    resp = httpx.get(url, headers=_HEADERS, timeout=settings.fetch_timeout_seconds, follow_redirects=True)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")
    results = []

    for item in soup.select(".vrwrap, .rb")[:settings.search_max_results]:
        link = item.select_one("h3 a")
        if not link:
            continue
        title = link.get_text(strip=True)
        href = link.get("href", "")
        snippet_el = item.select_one(".str_info, .space-txt, .ft")
        snippet = snippet_el.get_text(strip=True) if snippet_el else ""

        if title and href:
            if href.startswith("/"):
                href = f"https://www.sogou.com{href}"
            results.append({"title": title, "url": href, "snippet": snippet})

    return results


def _search_google(query: str) -> list[dict[str, str]]:
    """Search via Google."""
    url = f"https://www.google.com/search?q={quote_plus(query)}&num={settings.search_max_results}"
    resp = httpx.get(url, headers=_HEADERS, timeout=settings.fetch_timeout_seconds, follow_redirects=True)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")
    results = []

    for item in soup.select("div.g")[:settings.search_max_results]:
        link = item.select_one("a")
        if not link:
            continue
        title_el = item.select_one("h3")
        title = title_el.get_text(strip=True) if title_el else ""
        href = link.get("href", "")
        snippet_el = item.select_one("div.VwiC3b, span.aCOpRe")
        snippet = snippet_el.get_text(strip=True) if snippet_el else ""

        if title and href and href.startswith("http"):
            results.append({"title": title, "url": href, "snippet": snippet})

    return results


def _search_ddg(query: str) -> list[dict[str, str]]:
    """Search via DuckDuckGo HTML endpoint (fallback)."""
    url = "https://html.duckduckgo.com/html/"
    resp = httpx.post(url, data={"q": query}, headers=_HEADERS, timeout=settings.fetch_timeout_seconds, follow_redirects=True)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")
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
            # DDG redirect URLs: //duckduckgo.com/l/?uddg=...
            if "uddg=" in href:
                from urllib.parse import unquote, parse_qs, urlparse
                parsed = urlparse(href if href.startswith("http") else f"https:{href}")
                qs = parse_qs(parsed.query)
                href = unquote(qs.get("uddg", [href])[0])
            results.append({"title": title, "url": href, "snippet": snippet})

    return results


# Backward-compatible alias
search_ddg = search
