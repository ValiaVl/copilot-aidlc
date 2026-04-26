from app.services.article_service import create_article
from app.services.search_service import search
from app.services.user_service import get_or_create_user


def _setup(db):
    user = get_or_create_user(db, "alice")
    create_article(db, "FastAPI Guide", "How to build APIs with FastAPI", ["python", "fastapi"], user.id)
    create_article(db, "HTMX Basics", "Using HTMX for dynamic pages", ["htmx", "frontend"], user.id)
    create_article(db, "Go Tutorial", "Getting started with Go", ["go"], user.id)
    return user


def test_search_by_text(db):
    _setup(db)
    results = search(db, query="FastAPI")
    assert len(results) == 1
    assert results[0].title == "FastAPI Guide"


def test_search_by_text_case_insensitive(db):
    _setup(db)
    results = search(db, query="fastapi")
    assert len(results) == 1


def test_search_by_body(db):
    _setup(db)
    results = search(db, query="dynamic pages")
    assert len(results) == 1
    assert results[0].title == "HTMX Basics"


def test_search_by_tag(db):
    _setup(db)
    results = search(db, tag="python")
    assert len(results) == 1
    assert results[0].title == "FastAPI Guide"


def test_search_combined(db):
    _setup(db)
    results = search(db, query="guide", tag="python")
    assert len(results) == 1


def test_search_combined_no_match(db):
    _setup(db)
    results = search(db, query="Go", tag="python")
    assert len(results) == 0


def test_search_empty_returns_all(db):
    _setup(db)
    results = search(db)
    assert len(results) == 3
