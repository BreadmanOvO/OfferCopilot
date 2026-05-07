from typing import Any

from app.services.action_service import run_action_analysis
from app.services.research_service import run_research


def run_task_workflow(task_id: int, task_data: dict[str, Any]) -> dict[str, Any]:
    company = task_data.get("company_input", {}).get("company", "")
    intent = task_data.get("intent", {})
    jd_text = task_data.get("jd_text", "")
    user_links = task_data.get("user_links", [])
    resume_summary = task_data.get("resume_summary", "")
    concern_questions = task_data.get("concern_questions", [])

    if not company and not jd_text and not user_links:
        return {
            "status": "needs_input",
            "current_stage": "needs_input",
            "failure_reason": "No company name, JD text, or links provided. Please supply more information.",
        }

    research_result = run_research(
        company=company,
        intent=intent,
        jd_text=jd_text,
        user_links=user_links,
    )

    action_result = run_action_analysis(
        research=research_result["research"],
        resume_summary=resume_summary,
        concern_questions=concern_questions,
    )

    has_sufficient_sources = len(research_result["sources"]) >= 2
    status = "completed" if has_sufficient_sources else "partial_success"

    report = {**research_result["research"], **action_result}

    return {
        "status": status,
        "current_stage": "completed",
        "search_results": [],
        "sources": research_result["sources"],
        "failed_sources": research_result["failed_sources"],
        "uncertainty_notes": research_result["uncertainty_notes"],
        "research": research_result["research"],
        "action": action_result,
        "report": report,
        "failure_reason": "",
    }
