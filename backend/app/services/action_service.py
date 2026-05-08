from __future__ import annotations

import logging
from typing import Any

from app.tools.llm_client import llm
from app.tools.resume_parser import parse_resume_summary

logger = logging.getLogger(__name__)


def run_action_analysis(
    research: dict[str, Any],
    resume_summary: str,
    concern_questions: list[str],
) -> dict[str, Any]:
    # Try LLM-powered analysis first
    if llm.is_configured:
        try:
            return _llm_analysis(research, resume_summary, concern_questions)
        except Exception as e:
            logger.warning("LLM action analysis failed, falling back to rule-based: %s", e)

    # Fallback: keyword matching
    return _fallback_analysis(research, resume_summary, concern_questions)


def _llm_analysis(
    research: dict[str, Any],
    resume_summary: str,
    concern_questions: list[str],
) -> dict[str, Any]:
    jd = research.get("research", {}).get("jd_breakdown", {})
    company_profile = research.get("research", {}).get("company_profile", {})

    context_parts: list[str] = []

    # Company info
    company_summary = company_profile.get("summary", "")
    if company_summary:
        context_parts.append(f"【公司概况】\n{company_summary}")

    # JD info
    requirements = jd.get("requirements", [])
    responsibilities = jd.get("responsibilities", [])
    if requirements:
        context_parts.append(f"【岗位要求】\n" + "\n".join(requirements))
    if responsibilities:
        context_parts.append(f"【岗位职责】\n" + "\n".join(responsibilities))

    # Resume
    if resume_summary.strip():
        context_parts.append(f"【求职者简历摘要】\n{resume_summary}")
    else:
        context_parts.append("【求职者简历摘要】\n未提供")

    # Concern questions
    if concern_questions:
        context_parts.append(f"【求职者关心的问题】\n" + "\n".join(f"- {q}" for q in concern_questions))

    context_text = "\n\n".join(context_parts)

    messages = [
        {
            "role": "system",
            "content": (
                "你是一个资深的职业顾问。根据提供的公司信息、岗位要求和求职者背景，进行深度匹配分析。\n"
                "请用JSON格式返回，结构如下：\n"
                "{\n"
                '  "fit_analysis": {\n'
                '    "summary": "匹配度总结（100-200字）",\n'
                '    "match_score": 75,\n'
                '    "matched_strengths": ["优势1", "优势2"],\n'
                '    "gap_areas": ["差距1", "差距2"]\n'
                "  },\n"
                '  "skills_gap_summary": [\n'
                '    {"area": "技能领域", "severity": "high/medium/low", "suggestion": "提升建议"}\n'
                "  ],\n"
                '  "risks": ["风险提示1", "风险提示2"],\n'
                '  "interview_prep": [\n'
                '    {"question": "可能的面试问题", "suggestion": "回答建议"}\n'
                "  ],\n"
                '  "action_checklist": ["行动项1", "行动项2"]\n'
                "}\n"
                "只返回JSON，不要其他文字。用中文回答。"
            ),
        },
        {
            "role": "user",
            "content": context_text,
        },
    ]

    result = llm.chat_json(messages, max_tokens=2048)

    # Fill in interview prep for user's concern questions if LLM didn't cover them
    llm_prep = result.get("interview_prep", [])
    covered_qs = {p.get("question", "") for p in llm_prep}
    for q in concern_questions:
        if q not in covered_qs:
            llm_prep.append({"question": q, "suggestion": "请准备基于事实的回答"})

    return {
        "fit_analysis": result.get("fit_analysis", {}),
        "skills_gap_summary": result.get("skills_gap_summary", []),
        "risks": result.get("risks", []),
        "interview_prep": llm_prep,
        "action_checklist": result.get("action_checklist", []),
    }


def _fallback_analysis(
    research: dict[str, Any],
    resume_summary: str,
    concern_questions: list[str],
) -> dict[str, Any]:
    parsed_resume = parse_resume_summary(resume_summary)
    jd = research.get("research", {}).get("jd_breakdown", {})
    requirements = jd.get("requirements", [])
    company_summary = research.get("research", {}).get("company_profile", {}).get("summary", "")

    matched = [kw for kw in parsed_resume["keywords"] if any(kw in req.lower() for req in requirements)]
    gaps = [req for req in requirements if not any(kw in req.lower() for kw in parsed_resume["keywords"])]

    fit_analysis = {
        "summary": f"Based on {len(matched)} matching keywords and {len(gaps)} potential gaps.",
        "matched_keywords": matched,
        "gap_areas": gaps,
    }

    skills_gap = [{"area": gap, "severity": "medium"} for gap in gaps[:5]]

    risks = []
    if not company_summary:
        risks.append("Limited company information available.")
    if not requirements:
        risks.append("No clear requirements extracted from JD.")
    if not resume_summary:
        risks.append("No resume summary provided.")

    interview_prep = []
    for q in concern_questions:
        interview_prep.append({"question": q, "suggestion": f"Prepare evidence-based answer for: {q}"})

    action_checklist = [
        "Review the company profile and recent news",
        "Map your experience to each JD requirement",
        "Prepare 2-3 STAR stories for key skills",
        "Research the interview process on Glassdoor or similar",
    ]

    return {
        "fit_analysis": fit_analysis,
        "skills_gap_summary": skills_gap,
        "risks": risks,
        "interview_prep": interview_prep,
        "action_checklist": action_checklist,
    }
