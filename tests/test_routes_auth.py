import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


def test_signin_page(client):
    response = client.get("/signin")
    assert response.status_code == 200
    assert "Sign In" in response.text


def test_signin_creates_session(client):
    response = client.post("/signin", data={"name": "Alice"}, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/"


def test_signin_empty_name(client):
    response = client.post("/signin", data={"name": "   "})
    assert response.status_code == 422
    assert "Name is required" in response.text


def test_signout(client):
    client.post("/signin", data={"name": "Alice"})
    response = client.get("/signout", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/signin"


def test_home_redirects_when_not_signed_in(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 303
    assert "/signin" in response.headers["location"]
