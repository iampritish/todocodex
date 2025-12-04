import json

import pytest

from app import create_app, db, Todo


@pytest.fixture()
def client():
    app = create_app(testing=True)
    app.config.update(TESTING=True)

    with app.test_client() as client:
        with app.app_context():
            yield client


def test_create_and_list(client):
    res = client.post("/api/todos", json={"title": "Write tests"})
    assert res.status_code == 201
    payload = res.get_json()
    assert payload["title"] == "Write tests"

    res = client.get("/api/todos")
    assert res.status_code == 200
    todos = res.get_json()
    assert len(todos) == 1
    assert todos[0]["title"] == "Write tests"


def test_toggle_and_delete(client):
    res = client.post("/api/todos", json={"title": "Toggle me"})
    todo_id = res.get_json()["id"]

    res = client.patch(f"/api/todos/{todo_id}", json={"completed": True})
    assert res.status_code == 200
    assert res.get_json()["completed"] is True

    res = client.delete(f"/api/todos/{todo_id}")
    assert res.status_code == 204

    res = client.get("/api/todos")
    assert res.status_code == 200
    assert res.get_json() == []


def test_reject_empty_title(client):
    res = client.post("/api/todos", json={"title": "   "})
    assert res.status_code == 400
    assert res.get_json()["error"]

    res = client.post("/api/todos", data=json.dumps({}), content_type="application/json")
    assert res.status_code == 400
