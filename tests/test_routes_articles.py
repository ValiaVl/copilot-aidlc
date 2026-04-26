import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as c:
        c.post("/signin", data={"name": "TestUser"})
        yield c


def test_create_article(client):
    response = client.post(
        "/articles",
        data={"title": "Test Article", "body": "Some **markdown** body", "tags": ["python", "test"]},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert "/articles/" in response.headers["location"]


def test_create_article_missing_title(client):
    response = client.post("/articles", data={"title": "", "body": "Body"})
    assert response.status_code == 422
    assert "Title is required" in response.text


def test_create_article_missing_body(client):
    response = client.post("/articles", data={"title": "Title", "body": ""})
    assert response.status_code == 422
    assert "Body is required" in response.text


def test_view_article(client):
    resp = client.post(
        "/articles",
        data={"title": "View Test", "body": "Body content"},
        follow_redirects=False,
    )
    article_url = resp.headers["location"]
    response = client.get(article_url)
    assert response.status_code == 200
    assert "View Test" in response.text


def test_edit_article(client):
    resp = client.post("/articles", data={"title": "Original", "body": "Original body"}, follow_redirects=False)
    article_url = resp.headers["location"]
    response = client.post(
        f"{article_url}/edit",
        data={"title": "Updated", "body": "Updated body", "tags": ["edited"]},
        follow_redirects=False,
    )
    assert response.status_code == 303


def test_toggle_stale(client):
    resp = client.post("/articles", data={"title": "Stale Test", "body": "Body"}, follow_redirects=False)
    article_url = resp.headers["location"]
    response = client.post(f"{article_url}/stale")
    assert response.status_code == 200


def test_article_not_found(client):
    response = client.get("/articles/999")
    assert response.status_code == 404


def test_home_lists_articles(client):
    client.post("/articles", data={"title": "Listed Article", "body": "Body"}, follow_redirects=False)
    response = client.get("/")
    assert response.status_code == 200
    assert "Listed Article" in response.text
