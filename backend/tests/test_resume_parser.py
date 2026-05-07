from app.tools.resume_parser import parse_resume_summary


def test_parse_resume_extracts_keywords():
    result = parse_resume_summary("Built Python data systems and AI tooling for 3 years")
    assert "python" in result["keywords"]
    assert "built" in result["keywords"]


def test_parse_resume_empty():
    result = parse_resume_summary("")
    assert result["keywords"] == []
