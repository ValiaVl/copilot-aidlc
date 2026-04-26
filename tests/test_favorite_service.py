from app.services.article_service import create_article
from app.services.favorite_service import (
    get_favorite_count,
    get_favorite_counts,
    get_user_favorite_ids,
    is_favorited,
    list_favorites,
    toggle_favorite,
)
from app.services.user_service import get_or_create_user


def _make_user(db, name="alice"):
    return get_or_create_user(db, name)


def _make_article(db, user, title="Test Article"):
    return create_article(db, title, "Body text", [], user.id)


def test_toggle_favorite_on(db):
    user = _make_user(db)
    article = _make_article(db, user)
    returned_article, now_fav = toggle_favorite(db, user.id, article.id)
    assert returned_article is not None
    assert now_fav is True
    assert is_favorited(db, user.id, article.id) is True


def test_toggle_favorite_off(db):
    user = _make_user(db)
    article = _make_article(db, user)
    toggle_favorite(db, user.id, article.id)  # on
    _, now_fav = toggle_favorite(db, user.id, article.id)  # off
    assert now_fav is False
    assert is_favorited(db, user.id, article.id) is False


def test_toggle_favorite_article_not_found(db):
    user = _make_user(db)
    article, now_fav = toggle_favorite(db, user.id, 999)
    assert article is None
    assert now_fav is False


def test_is_favorited(db):
    user = _make_user(db)
    article = _make_article(db, user)
    assert is_favorited(db, user.id, article.id) is False
    toggle_favorite(db, user.id, article.id)
    assert is_favorited(db, user.id, article.id) is True


def test_get_favorite_count(db):
    user1 = _make_user(db, "alice")
    user2 = _make_user(db, "bob")
    article = _make_article(db, user1)
    assert get_favorite_count(db, article.id) == 0
    toggle_favorite(db, user1.id, article.id)
    assert get_favorite_count(db, article.id) == 1
    toggle_favorite(db, user2.id, article.id)
    assert get_favorite_count(db, article.id) == 2


def test_get_favorite_counts_batch(db):
    user = _make_user(db)
    a1 = _make_article(db, user, "Article 1")
    a2 = _make_article(db, user, "Article 2")
    toggle_favorite(db, user.id, a1.id)
    counts = get_favorite_counts(db, [a1.id, a2.id])
    assert counts.get(a1.id) == 1
    assert counts.get(a2.id) is None  # 0 favorites, not in result


def test_get_user_favorite_ids(db):
    user = _make_user(db)
    a1 = _make_article(db, user, "Article 1")
    a2 = _make_article(db, user, "Article 2")
    toggle_favorite(db, user.id, a1.id)
    ids = get_user_favorite_ids(db, user.id)
    assert ids == {a1.id}
    toggle_favorite(db, user.id, a2.id)
    ids = get_user_favorite_ids(db, user.id)
    assert ids == {a1.id, a2.id}


def test_list_favorites_ordered_by_recent(db):
    user = _make_user(db)
    a1 = _make_article(db, user, "First")
    a2 = _make_article(db, user, "Second")
    toggle_favorite(db, user.id, a1.id)
    toggle_favorite(db, user.id, a2.id)
    favs = list_favorites(db, user.id)
    assert len(favs) == 2
    assert favs[0].title == "Second"  # most recently favorited first
    assert favs[1].title == "First"


def test_list_favorites_empty(db):
    user = _make_user(db)
    assert list_favorites(db, user.id) == []
