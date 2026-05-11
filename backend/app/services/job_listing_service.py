from __future__ import annotations

import logging
import re
from typing import Any

import httpx
from bs4 import BeautifulSoup

from app.config import settings
from app.tools.llm_client import llm
from app.tools.search import search

logger = logging.getLogger(__name__)

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def _resolve_redirect_url(url: str) -> str:
    """Resolve Sogou/redirect URLs to the actual destination URL."""
    if "sogou.com/link" not in url:
        return url

    try:
        resp = httpx.get(url, headers=_HEADERS, timeout=settings.fetch_timeout_seconds, follow_redirects=True)
        soup = BeautifulSoup(resp.text, "lxml")

        # Try meta refresh
        meta = soup.find("meta", attrs={"http-equiv": "refresh"})
        if meta:
            content = meta.get("content", "")
            match = re.search(r"URL=['\"]?([^'\"]+)", content, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        # Try JS redirect
        for script in soup.find_all("script"):
            text = script.string or ""
            match = re.search(r'(?:window\.location(?:\.href)?|location)\s*[=.]\s*["\']([^"\']+)', text)
            if match:
                return match.group(1).strip()

    except Exception as e:
        logger.debug("Failed to resolve redirect for %s: %s", url, e)

    return url


def fetch_company_jobs(company_name: str) -> dict[str, Any]:
    """Fetch job listings for a company.

    Searches for recruitment info and extracts job listings via LLM
    using search snippets directly (no page fetching for speed).
    """
    # Search for recruitment info
    query = f"{company_name} 招聘 社招 岗位"
    search_results = search(query)

    if not search_results:
        return {"recruit_url": "", "positions": []}

    # Identify recruitment URL (only resolve the first one for speed)
    recruit_url = _find_recruit_url(company_name, search_results)
    if "sogou.com/link" in recruit_url:
        recruit_url = _resolve_redirect_url(recruit_url)

    # Build context from search results (use snippets directly for speed)
    context_parts: list[str] = []
    for result in search_results[:6]:
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        url = result.get("url", "")
        if snippet:
            # Resolve URL for display
            real_url = url
            if "sogou.com/link" in url:
                try:
                    real_url = _resolve_redirect_url(url)
                except Exception:
                    real_url = url
            context_parts.append(f"来源: {title}\n链接: {real_url}\n摘要: {snippet}")

    if not context_parts:
        return {"recruit_url": recruit_url, "positions": []}

    # Extract jobs via LLM
    if llm.is_configured:
        try:
            return _llm_extract_jobs(company_name, recruit_url, context_parts)
        except Exception as e:
            logger.warning("LLM job extraction failed: %s", e)

    return {"recruit_url": recruit_url, "positions": []}


def _find_recruit_url(company_name: str, results: list[dict[str, str]]) -> str:
    """Find the company's recruitment website from search results."""
    for r in results:
        url = r.get("url", "").lower()
        title = r.get("title", "")
        if any(kw in url for kw in ["career", "jobs", "zhaopin", "recruit"]):
            return r["url"]
        if "招聘" in title and ("官网" in title or "官方" in title):
            return r["url"]

    from app.tools.link_classifier import classify_url
    for r in results:
        url = r.get("url", "")
        if url and classify_url(url) != "job_board":
            return url

    return results[0]["url"] if results else ""


def _llm_extract_jobs(
    company_name: str,
    recruit_url: str,
    context_parts: list[str],
) -> dict[str, Any]:
    """Use LLM to extract job listings from search context."""
    context = "\n\n---\n\n".join(context_parts[:6])

    messages = [
        {
            "role": "system",
            "content": (
                "你是一个招聘信息分析专家。根据搜索结果摘要，提取公司的在招岗位信息。\n"
                "请返回JSON格式：\n"
                "{\n"
                '  "recruit_url": "公司招聘官网URL（如有）",\n'
                '  "positions": [\n'
                '    {"title": "岗位名称", "url": "岗位详情链接(如有)", "location": "工作城市", "department": "所属部门(如有)"}\n'
                "  ]\n"
                "}\n"
                "从搜索摘要中提取提到的具体岗位名称。如果摘要中提到了岗位，就提取出来。\n"
                "如果找不到具体岗位信息，返回空数组。\n"
                "只返回JSON，不要其他文字。"
            ),
        },
        {
            "role": "user",
            "content": f"公司: {company_name}\n已知招聘官网: {recruit_url}\n\n以下是搜索结果摘要：\n\n{context}",
        },
    ]

    result = llm.chat_json(messages, max_tokens=2048, temperature=0.3)

    positions = result.get("positions", [])
    cleaned_positions = []
    for pos in positions[:10]:
        if isinstance(pos, dict) and pos.get("title"):
            cleaned_positions.append({
                "title": str(pos["title"]),
                "url": str(pos.get("url", "")),
                "location": str(pos.get("location", "")),
                "department": str(pos.get("department", "")),
            })

    return {
        "recruit_url": result.get("recruit_url", recruit_url) or recruit_url,
        "positions": cleaned_positions,
    }
