import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as c:
        c.post("/signin", data={"name": "SearchUser"})
        c.post("/articles", data={"title": "Python Guide", "body": "Learn Python", "tags": ["python"]}, follow_redirects=True)
        c.post("/articles", data={"title": "Go Guide", "body": "Learn Go", "tags": ["go"]}, follow_redirects=True)
        yield c


def test_search_by_text(client):
    response = client.get("/search?q=Python")
    assert response.status_code == 200
    assert "Python Guide" in response.text


def test_search_by_tag(client):
    response = client.get("/search?tag=go")
    assert response.status_code == 200
    assert "Go Guide" in response.text


def test_search_empty(client):
    response = client.get("/search")
    assert response.status_code == 200
