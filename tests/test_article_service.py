from app.services.article_service import (
    create_article,
    get_article,
    get_edit_log,
    list_articles,
    toggle_stale,
    update_article,
)
from app.services.user_service import get_or_create_user


def _make_user(db, name="alice"):
    return get_or_create_user(db, name)


def test_create_article(db):
    user = _make_user(db)
    article = create_article(db, "Title", "Body text", ["python", "fastapi"], user.id)
    assert article.id is not None
    assert article.title == "Title"
    assert article.author_id == user.id
    assert len(article.tags) == 2


def test_get_article(db):
    user = _make_user(db)
    created = create_article(db, "Title", "Body", [], user.id)
    found = get_article(db, created.id)
    assert found is not None
    assert found.title == "Title"
    assert found.author.name == "alice"


def test_get_article_not_found(db):
    assert get_article(db, 999) is None


def test_update_article(db):
    user = _make_user(db)
    article = create_article(db, "Old Title", "Old Body", ["old"], user.id)
    editor = _make_user(db, "bob")
    updated = update_article(db, article.id, "New Title", "New Body", ["new"], editor.id)
    assert updated.title == "New Title"
    assert len(updated.tags) == 1
    assert updated.tags[0].name == "new"


def test_update_creates_edit_log(db):
    user = _make_user(db)
    article = create_article(db, "Title", "Body", [], user.id)
    editor = _make_user(db, "bob")
    update_article(db, article.id, "Title2", "Body2", [], editor.id)
    logs = get_edit_log(db, article.id)
    assert len(logs) == 1
    assert logs[0].editor.name == "bob"


def test_list_articles(db):
    user = _make_user(db)
    create_article(db, "A", "Body A", ["python"], user.id)
    create_article(db, "B", "Body B", ["go"], user.id)
    articles = list_articles(db)
    assert len(articles) == 2


def test_list_articles_filter_by_tag(db):
    user = _make_user(db)
    create_article(db, "A", "Body A", ["python"], user.id)
    create_article(db, "B", "Body B", ["go"], user.id)
    articles = list_articles(db, tag="python")
    assert len(articles) == 1
    assert articles[0].title == "A"


def test_toggle_stale(db):
    user = _make_user(db)
    article = create_article(db, "Title", "Body", [], user.id)
    assert article.is_stale is False
    toggled = toggle_stale(db, article.id)
    assert toggled.is_stale is True
    toggled2 = toggle_stale(db, article.id)
    assert toggled2.is_stale is False


def test_toggle_stale_not_found(db):
    assert toggle_stale(db, 999) is None


def test_tag_deduplication(db):
    user = _make_user(db)
    create_article(db, "A", "Body", ["python"], user.id)
    create_article(db, "B", "Body", ["python"], user.id)
    from app.models.tag import Tag

    tags = db.query(Tag).filter(Tag.name == "python").all()
    assert len(tags) == 1
