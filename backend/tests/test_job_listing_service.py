import app.services.job_listing_service as job_listing_service


def test_fetch_company_jobs_returns_empty_message_when_no_results(monkeypatch):
    monkeypatch.setattr(job_listing_service, "search", lambda query: [])

    result = job_listing_service.fetch_company_jobs("测试公司")

    assert result["recruit_url"] == ""
    assert result["positions"] == []
    assert result["message"] == "未找到招聘相关搜索结果"
    assert result["confidence"] == "low"


def test_fetch_company_jobs_returns_official_site_message_when_no_positions(monkeypatch):
    monkeypatch.setattr(
        job_listing_service,
        "search",
        lambda query: [
            {
                "title": "某公司招聘官网",
                "snippet": "欢迎访问招聘官网，查看社会招聘岗位。",
                "url": "https://example.com/jobs",
            }
        ],
    )

    class StubLLM:
        is_configured = True

        @staticmethod
        def chat_json(messages, max_tokens=2048, temperature=0.3):
            return {
                "recruit_url": "https://example.com/jobs",
                "positions": [],
            }

    monkeypatch.setattr(job_listing_service, "llm", StubLLM())

    result = job_listing_service.fetch_company_jobs("某公司")

    assert result["recruit_url"] == "https://example.com/jobs"
    assert result["positions"] == []
    assert "招聘官网" in result["message"]
    assert "未提取到" in result["message"]
    assert result["confidence"] in {"low", "medium"}
