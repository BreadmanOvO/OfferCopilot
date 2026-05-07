from app.services.action_service import run_action_analysis


def test_action_analysis_returns_structured_output():
    research = {
        "company_profile": {"summary": "AI company"},
        "jd_breakdown": {"requirements": ["Python", "LLM experience"]},
        "sources": [],
        "uncertainty_notes": [],
    }
    result = run_action_analysis(research, "Built Python AI systems", ["Am I a fit?"])
    assert result["fit_analysis"]
    assert result["action_checklist"]
    assert result["interview_prep"]


def test_action_analysis_handles_empty_research():
    result = run_action_analysis({}, "", [])
    assert result["fit_analysis"]
    assert "risks" in result
