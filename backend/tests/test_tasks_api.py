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
