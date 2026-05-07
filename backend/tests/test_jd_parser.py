from app.tools.jd_parser import parse_jd


def test_parse_jd_extracts_requirements():
    jd = "Requirements:\n- 3+ years Python\n- Experience with LLMs\nResponsibilities:\n- Build agent systems"
    result = parse_jd(jd)
    assert len(result["requirements"]) >= 1
    assert len(result["responsibilities"]) >= 1


def test_parse_jd_empty():
    result = parse_jd("")
    assert result["requirements"] == []
