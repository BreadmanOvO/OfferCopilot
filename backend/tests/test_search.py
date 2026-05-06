from app.tools.search import generate_search_queries


def test_generate_search_queries():
    queries = generate_search_queries(
        company="Anthropic",
        intent={"city": "San Francisco", "target_role": "Engineer"},
        jd_text="Build Claude tools",
    )
    assert len(queries) >= 3
    assert any("Anthropic" in q for q in queries)
