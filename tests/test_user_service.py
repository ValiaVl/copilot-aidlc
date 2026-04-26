from app.services.user_service import get_or_create_user, get_user_by_id


def test_create_new_user(db):
    user = get_or_create_user(db, "Alice")
    assert user.name == "alice"
    assert user.id is not None


def test_get_existing_user(db):
    user1 = get_or_create_user(db, "Alice")
    user2 = get_or_create_user(db, "alice")
    assert user1.id == user2.id


def test_case_insensitive(db):
    user1 = get_or_create_user(db, "ALICE")
    user2 = get_or_create_user(db, "alice")
    assert user1.id == user2.id


def test_strips_whitespace(db):
    user = get_or_create_user(db, "  Bob  ")
    assert user.name == "bob"


def test_get_user_by_id(db):
    user = get_or_create_user(db, "Alice")
    found = get_user_by_id(db, user.id)
    assert found is not None
    assert found.name == "alice"


def test_get_user_by_id_not_found(db):
    assert get_user_by_id(db, 999) is None
