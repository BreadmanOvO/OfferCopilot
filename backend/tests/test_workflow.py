from unittest.mock import patch

from app.workflows.task_workflow import run_task_workflow


@patch("app.services.research_service.search_ddg")
@patch("app.services.research_service.fetch_page_content")
def test_run_workflow_direct_path(mock_fetch, mock_search):
    mock_search.return_value = [
        {"title": "TestCo", "url": "https://testco.com", "snippet": "AI company"},
        {"title": "TestCo Jobs", "url": "https://testco.com/careers", "snippet": "Hiring"},
        {"title": "TestCo News", "url": "https://news.com/testco", "snippet": "Growing"},
    ]
    mock_fetch.return_value = {"url": "https://testco.com", "title": "TestCo", "content": "We build AI.", "error": ""}

    result = run_task_workflow(1, {
        "company_input": {"company": "TestCo"},
        "intent": {},
        "jd_text": "Build AI systems with Python",
        "user_links": [],
        "resume_summary": "3 years Python AI",
        "concern_questions": ["Am I qualified?"],
    })

    assert result["status"] in ("completed", "partial_success")
    assert result["sources"]
    assert result["report"]["fit_analysis"]


@patch("app.services.research_service.search_ddg")
def test_workflow_needs_input_when_no_company_or_jd(mock_search):
    mock_search.return_value = []
    result = run_task_workflow(1, {"company_input": {}, "intent": {}, "jd_text": "", "user_links": [], "resume_summary": "", "concern_questions": []})
    assert result["status"] == "needs_input"
