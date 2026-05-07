from unittest.mock import patch

from app.services.research_service import run_research


@patch("app.services.research_service.search_ddg")
@patch("app.services.research_service.fetch_page_content")
def test_run_research_returns_structured_output(mock_fetch, mock_search):
    mock_search.return_value = [
        {"title": "Anthropic", "url": "https://anthropic.com", "snippet": "AI safety"},
    ]
    mock_fetch.return_value = {"url": "https://anthropic.com", "title": "Anthropic", "content": "We build Claude.", "error": ""}

    result = run_research(company="Anthropic", intent={}, jd_text="Build agents", user_links=[])

    assert result["sources"]
    assert result["research"]["company_profile"]
    assert result["research"]["jd_breakdown"]


@patch("app.services.research_service.search_ddg")
def test_run_research_with_no_search_results(mock_search):
    mock_search.return_value = []

    result = run_research(company="UnknownCorp", intent={}, jd_text="", user_links=[])

    assert result["research"]["confidence"] == "low"
    assert len(result["uncertainty_notes"]) > 0
