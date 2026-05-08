from __future__ import annotations

import logging
from typing import Any

import httpx
from bs4 import BeautifulSoup

from app.config import settings
from app.tools.llm_client import llm

logger = logging.getLogger(__name__)


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
