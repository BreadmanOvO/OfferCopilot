from unittest.mock import patch

from app.schemas import CreateTaskRequest


def test_create_task_request_defaults():
    request = CreateTaskRequest(
        mode="intent",
        intent={"city": "Shanghai", "role": "LLM Engineer"},
        company_input={},
    )
    assert request.mode == "intent"
    assert request.jd_text == ""
    assert request.user_links == []


def test_create_intent_task(client):
    response = client.post(
        "/tasks",
        json={
            "mode": "intent",
            "intent": {"city": "Shanghai", "target_role": "LLM Engineer"},
            "company_input": {},
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
    assert data["mode"] == "intent"


def test_get_task(client):
    created = client.post(
        "/tasks",
        json={"mode": "direct", "intent": {}, "company_input": {"company": "Test"}},
    ).json()

    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_task_not_found(client):
    response = client.get("/tasks/99999")
    assert response.status_code == 404


def test_create_intent_task_returns_company_options(client):
    response = client.post(
        "/tasks",
        json={
            "mode": "intent",
            "intent": {"city": "Shanghai", "target_role": "LLM Engineer"},
            "company_input": {},
        },
    )
    data = response.json()
    assert data["report"]["company_options"]
    assert len(data["report"]["company_options"]) >= 1


@patch("app.services.research_service.search_ddg")
@patch("app.services.research_service.fetch_page_content")
def test_run_direct_task(mock_fetch, mock_search, client):
    mock_search.return_value = [
        {"title": "Test", "url": "https://test.com/1", "snippet": "A"},
        {"title": "Test", "url": "https://test.com/2", "snippet": "B"},
        {"title": "Test", "url": "https://test.com/3", "snippet": "C"},
    ]
    mock_fetch.return_value = {"url": "https://test.com", "title": "Test", "content": "AI company.", "error": ""}

    created = client.post("/tasks", json={
        "mode": "direct",
        "intent": {},
        "company_input": {"company": "TestCo"},
        "jd_text": "Build AI with Python",
        "resume_summary": "Python AI experience",
    }).json()

    response = client.post(f"/tasks/{created['id']}/run")
    data = response.json()

    assert response.status_code == 200
    assert data["status"] in ("completed", "partial_success")
    assert data["report"]["fit_analysis"]


def test_run_task_not_found(client):
    response = client.post("/tasks/99999/run")
    assert response.status_code == 404


def test_append_inputs(client):
    created = client.post("/tasks", json={"mode": "direct", "intent": {}, "company_input": {"company": "Test"}}).json()

    response = client.post(f"/tasks/{created['id']}/inputs", json={
        "user_links": ["https://test.com/jobs"],
        "jd_text": "New JD content",
    })
    assert response.status_code == 200
    data = response.json()
    assert "https://test.com/jobs" in data["user_links"]
    assert "New JD" in data["jd_text"]
