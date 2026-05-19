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


def test_extract_positions_from_recruit_page_html():
    html = """
    <html>
      <body>
        <nav><a href="/login">登录</a></nav>
        <section>
          <a href="/jobs/backend-engineer">后端开发工程师</a>
          <a href="/jobs/product-manager">产品经理</a>
          <a href="/about">关于我们</a>
        </section>
      </body>
    </html>
    """

    positions = job_listing_service._extract_positions_from_html(
        html,
        base_url="https://example.com/careers",
    )

    assert positions == [
        {
            "title": "后端开发工程师",
            "url": "https://example.com/jobs/backend-engineer",
            "location": "",
            "department": "",
            "description": "",
            "requirements": "",
            "source": "https://example.com/careers",
        },
        {
            "title": "产品经理",
            "url": "https://example.com/jobs/product-manager",
            "location": "",
            "department": "",
            "description": "",
            "requirements": "",
            "source": "https://example.com/careers",
        },
    ]


def test_fetch_company_jobs_uses_recruit_page_html(monkeypatch):
    monkeypatch.setattr(
        job_listing_service,
        "search",
        lambda query: [
            {
                "title": "某公司招聘官网",
                "snippet": "查看某公司社会招聘岗位。",
                "url": "https://example.com/careers",
            }
        ],
    )

    class StubResponse:
        text = """
        <html><body>
          <a href="/jobs/backend-engineer">后端开发工程师</a>
        </body></html>
        """

        def raise_for_status(self):
            return None

    monkeypatch.setattr(job_listing_service.httpx, "get", lambda *args, **kwargs: StubResponse())

    result = job_listing_service.fetch_company_jobs("某公司")

    assert result["recruit_url"] == "https://example.com/careers"
    assert result["positions"][0]["title"] == "后端开发工程师"
    assert result["positions"][0]["url"] == "https://example.com/jobs/backend-engineer"
    assert "招聘页" in result["message"]
    assert result["confidence"] == "medium"


def test_enrich_positions_from_detail_pages(monkeypatch):
    positions = [
        {
            "title": "后端开发工程师",
            "url": "https://example.com/jobs/backend-engineer",
            "location": "",
            "department": "",
            "description": "",
            "requirements": "",
            "source": "https://example.com/careers",
        }
    ]

    def fake_fetch_html(url):
        assert url == "https://example.com/jobs/backend-engineer"
        return """
        <html><body>
          <h1>后端开发工程师</h1>
          <p>工作地点：上海</p>
          <section>岗位描述：负责核心服务开发和稳定性建设。</section>
          <section>岗位要求：熟悉 Python 和 FastAPI。</section>
        </body></html>
        """

    monkeypatch.setattr(job_listing_service, "_fetch_html", fake_fetch_html)

    enriched = job_listing_service._enrich_positions_from_detail_pages(positions)

    assert enriched[0]["location"] == "上海"
    assert "核心服务开发" in enriched[0]["description"]
    assert "Python" in enriched[0]["requirements"]
    assert enriched[0]["source"] == "https://example.com/jobs/backend-engineer"


def test_fetch_company_jobs_explains_inaccessible_recruit_page(monkeypatch):
    monkeypatch.setattr(
        job_listing_service,
        "search",
        lambda query: [
            {
                "title": "某公司招聘官网",
                "snippet": "查看某公司社会招聘岗位。",
                "url": "https://example.com/careers",
            }
        ],
    )

    def fake_get(*args, **kwargs):
        raise job_listing_service.httpx.HTTPError("network failed")

    monkeypatch.setattr(job_listing_service.httpx, "get", fake_get)

    class StubLLM:
        is_configured = False

    monkeypatch.setattr(job_listing_service, "llm", StubLLM())

    result = job_listing_service.fetch_company_jobs("某公司")

    assert result["recruit_url"] == "https://example.com/careers"
    assert result["positions"] == []
    assert "招聘页暂时不可访问" in result["message"]
    assert result["confidence"] == "low"
