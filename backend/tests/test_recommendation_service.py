from app.services.recommendation_service import recommend_companies


def test_recommend_companies_returns_results():
    results = recommend_companies(
        {"city": "Shanghai", "target_role": "LLM Engineer", "technical_field": "LLM", "company_type": "startup"}
    )
    assert len(results) >= 1
    assert results[0]["company_name"]
    assert results[0]["reason"]


def test_recommend_companies_with_minimal_input():
    results = recommend_companies({})
    assert len(results) >= 1
