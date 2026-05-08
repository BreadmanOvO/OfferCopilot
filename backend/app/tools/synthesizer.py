from __future__ import annotations

import logging
from typing import Any

from app.config import settings
from app.tools.llm_client import llm

logger = logging.getLogger(__name__)


def synthesize_research(
    sources: list[dict[str, Any]],
    page_contents: list[dict[str, Any]],
    jd_breakdown: dict[str, Any],
    uncertainty_notes: list[str],
) -> dict[str, Any]:
    if len(sources) < settings.min_sources_for_confident_report:
        return {
            "company_profile": {"summary": "Insufficient sources to form a confident company profile."},
            "jd_breakdown": jd_breakdown,
            "sources": sources,
            "uncertainty_notes": uncertainty_notes + ["Not enough sources found. Please provide company links or JD text."],
            "confidence": "low",
        }

    # Try LLM-powered synthesis first
    if llm.is_configured:
        try:
            return _llm_synthesize(sources, page_contents, jd_breakdown, uncertainty_notes)
        except Exception as e:
            logger.warning("LLM synthesis failed, falling back to rule-based: %s", e)

    # Fallback: simple concatenation
    return _fallback_synthesize(sources, page_contents, jd_breakdown, uncertainty_notes)


def _llm_synthesize(
    sources: list[dict[str, Any]],
    page_contents: list[dict[str, Any]],
    jd_breakdown: dict[str, Any],
    uncertainty_notes: list[str],
) -> dict[str, Any]:
    # Build context from fetched pages
    context_parts: list[str] = []
    for i, (src, page) in enumerate(zip(sources, page_contents)):
        content = (page.get("content") or "")[:2000]
        if content:
            context_parts.append(f"[Source {i+1}: {src.get('title', 'N/A')}]\n{content}")

    if not context_parts:
        return _fallback_synthesize(sources, page_contents, jd_breakdown, uncertainty_notes)

    source_text = "\n\n---\n\n".join(context_parts[:5])

    messages = [
        {
            "role": "system",
            "content": (
                "你是一个专业的公司研究分析师。根据提供的网页内容，提取并综合公司的关键信息。\n"
                "请用JSON格式返回，结构如下：\n"
                "{\n"
                '  "company_profile": {\n'
                '    "summary": "公司概况（200-400字）",\n'
                '    "industry": "所属行业",\n'
                '    "scale": "公司规模",\n'
                '    "culture": "企业文化特点",\n'
                '    "tech_stack": ["技术栈1", "技术栈2"],\n'
                '    "benefits": ["福利1", "福利2"],\n'
                '    "recent_news": ["近期动态1"]\n'
                "  },\n"
                '  "confidence": "high/medium/low"\n'
                "}\n"
                "只返回JSON，不要其他文字。"
            ),
        },
        {
            "role": "user",
            "content": f"以下是关于该公司的网页内容：\n\n{source_text}",
        },
    ]

    result = llm.chat_json(messages, max_tokens=2048)

    return {
        "company_profile": result.get("company_profile", {"summary": "LLM returned empty profile."}),
        "jd_breakdown": jd_breakdown,
        "sources": sources,
        "uncertainty_notes": uncertainty_notes,
        "confidence": result.get("confidence", "medium"),
    }


def _fallback_synthesize(
    sources: list[dict[str, Any]],
    page_contents: list[dict[str, Any]],
    jd_breakdown: dict[str, Any],
    uncertainty_notes: list[str],
) -> dict[str, Any]:
    page_summaries = [p["content"][:300] for p in page_contents if p.get("content")]
    combined_summary = "\n\n".join(page_summaries[:3]) if page_summaries else "No page content extracted."

    return {
        "company_profile": {"summary": combined_summary},
        "jd_breakdown": jd_breakdown,
        "sources": sources,
        "uncertainty_notes": uncertainty_notes,
        "confidence": "medium",
    }
