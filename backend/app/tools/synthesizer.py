from typing import Any

from app.config import settings


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

    page_summaries = [p["content"][:300] for p in page_contents if p.get("content")]
    combined_summary = "\n\n".join(page_summaries[:3]) if page_summaries else "No page content extracted."

    return {
        "company_profile": {"summary": combined_summary},
        "jd_breakdown": jd_breakdown,
        "sources": sources,
        "uncertainty_notes": uncertainty_notes,
        "confidence": "medium",
    }
