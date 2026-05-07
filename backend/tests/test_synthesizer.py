from app.tools.synthesizer import synthesize_research


def test_synthesize_with_sufficient_sources():
    sources = [
        {"title": "Company", "url": "https://example.com/1", "snippet": "A"},
        {"title": "Careers", "url": "https://example.com/2", "snippet": "B"},
        {"title": "Jobs", "url": "https://example.com/3", "snippet": "C"},
    ]
    pages = [{"content": "Company makes AI tools."}, {"content": "Hiring engineers."}, {"content": "Great culture."}]
    result = synthesize_research(sources, pages, {"requirements": ["Python"]}, [])
    assert result["confidence"] == "medium"
    assert result["company_profile"]["summary"]


def test_synthesize_with_insufficient_sources():
    result = synthesize_research([], [], {}, [])
    assert result["confidence"] == "low"
    assert "Insufficient" in result["company_profile"]["summary"]
