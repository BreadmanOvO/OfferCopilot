from typing import Any

from app.tools.resume_parser import parse_resume_summary


def run_action_analysis(
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
