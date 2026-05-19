from __future__ import annotations

import logging
import re
from typing import Any
from urllib.parse import urljoin, urlparse

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


_JOB_KEYWORDS = [
    "工程师",
    "开发",
    "产品",
    "运营",
    "实习",
    "后端",
    "前端",
    "算法",
    "数据",
    "测试",
    "backend",
    "frontend",
    "engineer",
    "developer",
    "manager",
    "intern",
]

_NOISE_KEYWORDS = [
    "登录",
    "注册",
    "首页",
    "关于",
    "隐私",
    "条款",
    "帮助",
    "校园招聘",
    "校招",
]


def _clean_text(value: str) -> str:
    return " ".join(value.split())


def _looks_like_job_title(text: str, href: str) -> bool:
    title = _clean_text(text)
    if len(title) < 2 or len(title) > 80:
        return False
    lowered = f"{title} {href}".lower()
    if any(keyword in title for keyword in _NOISE_KEYWORDS):
        return False
    return any(keyword in lowered for keyword in _JOB_KEYWORDS)


def _normalize_url(href: str, base_url: str) -> str:
    return urljoin(base_url, href)


def _extract_positions_from_html(html: str, base_url: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    positions: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for link in soup.find_all("a"):
        title = _clean_text(link.get_text(" "))
        href = str(link.get("href") or "")
        if not href or not _looks_like_job_title(title, href):
            continue

        url = _normalize_url(href, base_url)
        key = (title, url)
        if key in seen:
            continue
        seen.add(key)
        positions.append({
            "title": title,
            "url": url,
            "location": "",
            "department": "",
            "description": "",
            "requirements": "",
            "source": base_url,
        })

    return positions[:10]


def _fetch_html(url: str) -> str:
    resp = httpx.get(url, headers=_HEADERS, timeout=settings.fetch_timeout_seconds, follow_redirects=True)
    resp.raise_for_status()
    return resp.text


def _extract_labeled_value(text: str, labels: list[str]) -> str:
    stop_pattern = "|".join([
        "工作地点",
        "地点",
        "城市",
        "岗位描述",
        "职位描述",
        "工作职责",
        "岗位职责",
        "岗位要求",
        "任职要求",
        "职位要求",
    ])
    for label in labels:
        match = re.search(rf"{label}\s*[：:]\s*(.*?)(?=\s*(?:{stop_pattern})\s*[：:]|$)", text)
        if match:
            return match.group(1).strip(" 。；;")[:240]
    return ""


def _extract_detail_fields(html: str) -> dict[str, str]:
    soup = BeautifulSoup(html, "lxml")
    text = _clean_text(soup.get_text("\n"))
    return {
        "location": _extract_labeled_value(text, ["工作地点", "地点", "城市"])[:80],
        "department": "",
        "description": _extract_labeled_value(text, ["岗位描述", "职位描述", "工作职责", "岗位职责"]),
        "requirements": _extract_labeled_value(text, ["岗位要求", "任职要求", "职位要求"]),
    }


def _same_site(left_url: str, right_url: str) -> bool:
    left_host = urlparse(left_url).netloc
    right_host = urlparse(right_url).netloc
    return bool(left_host and right_host and left_host == right_host)


def _enrich_positions_from_detail_pages(positions: list[dict[str, str]]) -> list[dict[str, str]]:
    enriched = [dict(position) for position in positions]
    for position in enriched[:3]:
        url = position.get("url", "")
        source = position.get("source", "")
        if not url or not source or not _same_site(url, source):
            continue
        try:
            detail_html = _fetch_html(url)
            fields = _extract_detail_fields(detail_html)
        except Exception as e:
            logger.info("Failed to fetch job detail %s: %s", url, e)
            continue
        for key, value in fields.items():
            if value and not position.get(key):
                position[key] = value
        position["source"] = url
    return enriched


def fetch_company_jobs(company_name: str) -> dict[str, Any]:
    """Fetch job listings for a company.

    Searches for recruitment info and extracts job listings via LLM
    using search snippets directly (no page fetching for speed).
    """
    # Search for recruitment info
    query = f"{company_name} 招聘 社招 岗位"
    search_results = search(query)

    if not search_results:
        return {
            "recruit_url": "",
            "positions": [],
            "message": "未找到招聘相关搜索结果",
            "confidence": "low",
        }

    # Identify recruitment URL (only resolve the first one for speed)
    recruit_url = _find_recruit_url(company_name, search_results)
    if "sogou.com/link" in recruit_url:
        recruit_url = _resolve_redirect_url(recruit_url)

    crawl_failure_message = ""
    if recruit_url:
        try:
            recruit_html = _fetch_html(recruit_url)
            positions = _extract_positions_from_html(recruit_html, recruit_url)
            if positions:
                enriched_positions = _enrich_positions_from_detail_pages(positions)
                has_details = any(
                    position.get("description") or position.get("requirements")
                    for position in enriched_positions
                )
                return {
                    "recruit_url": recruit_url,
                    "positions": enriched_positions,
                    "message": (
                        f"已从招聘页识别 {len(enriched_positions)} 个岗位，并补充部分详情"
                        if has_details
                        else f"已从招聘页识别 {len(enriched_positions)} 个岗位，详情信息可能不完整"
                    ),
                    "confidence": "medium",
                }
        except Exception as e:
            logger.info("Failed to fetch recruit page %s: %s", recruit_url, e)
            crawl_failure_message = "招聘页暂时不可访问，请先访问招聘官网查看"

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
        return {
            "recruit_url": recruit_url,
            "positions": [],
            "message": "已找到招聘官网，但搜索结果未包含可提取的岗位摘要",
            "confidence": "low",
        }

    # Extract jobs via LLM
    if llm.is_configured:
        try:
            return _llm_extract_jobs(company_name, recruit_url, context_parts)
        except Exception as e:
            logger.warning("LLM job extraction failed: %s", e)

    if crawl_failure_message:
        return {
            "recruit_url": recruit_url,
            "positions": [],
            "message": crawl_failure_message,
            "confidence": "low",
        }

    return {
        "recruit_url": recruit_url,
        "positions": [],
        "message": "岗位提取暂时不可用，请先访问招聘官网查看",
        "confidence": "low",
    }


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
                '    {"title": "岗位名称", "url": "岗位详情链接(如有)", "location": "工作城市", "department": "所属部门(如有)", "description": "岗位描述摘要(如有)", "requirements": "岗位要求摘要(如有)", "source": "信息来源链接(如有)"}\n'
                "  ]\n"
                "}\n"
                "从搜索摘要中提取提到的具体岗位名称。如果摘要中提到了岗位，就提取出来。\n"
                "如果摘要中没有明确岗位描述或要求，不要编造，填空字符串。\n"
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
                "description": str(pos.get("description", "")),
                "requirements": str(pos.get("requirements", "")),
                "source": str(pos.get("source", recruit_url or "")),
            })

    resolved_recruit_url = result.get("recruit_url", recruit_url) or recruit_url
    return {
        "recruit_url": resolved_recruit_url,
        "positions": cleaned_positions,
        "message": f"已提取 {len(cleaned_positions)} 个岗位" if cleaned_positions else "已找到招聘官网，但未提取到具体岗位",
        "confidence": "medium" if cleaned_positions else "low",
    }
