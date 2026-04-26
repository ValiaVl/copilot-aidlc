# Unit Test Execution — Team Knowledge Base

## Run All Unit Tests

```bash
uv run pytest tests/ -v
```

## Run Specific Test Files

```bash
# Service tests
uv run pytest tests/test_user_service.py -v
uv run pytest tests/test_article_service.py -v
uv run pytest tests/test_search_service.py -v
uv run pytest tests/test_favorite_service.py -v

# Route tests
uv run pytest tests/test_routes_auth.py -v
uv run pytest tests/test_routes_articles.py -v
uv run pytest tests/test_routes_search.py -v
```

## Expected Results

### Service Tests
| File | Tests | Description |
|------|-------|-------------|
| `test_user_service.py` | 6 | User creation, case-insensitivity, whitespace trimming, lookup |
| `test_article_service.py` | 10 | Article CRUD, tag sync, edit log, stale toggle, tag deduplication |
| `test_search_service.py` | 7 | Text search, tag filter, combined search, case-insensitive, empty query |
| `test_favorite_service.py` | 9 | Toggle on/off, is_favorited, count, batch counts, user IDs, list ordering, empty list, not-found |

### Route Tests
| File | Tests | Description |
|------|-------|-------------|
| `test_routes_auth.py` | 5 | Sign-in page, session creation, empty name validation, sign-out, auth redirect |
| `test_routes_articles.py` | 13 | Article CRUD, validation, stale toggle, 404 handling, listing, favorite toggle on/off, auth check, hearts display, favorites filter, detail heart |
| `test_routes_search.py` | 3 | Text search, tag search, empty search |

**Total**: 54 tests, all should pass with 0 failures.

## Test Infrastructure
- Tests use **in-memory SQLite** (no file created)
- Each test gets a fresh database via the `db` fixture in `tests/conftest.py`
- Route tests use FastAPI's `TestClient` with a real HTTP session

## Fix Failing Tests
1. Read the test output carefully — pytest shows the assertion that failed
2. Check if the issue is in the test or the application code
3. Fix and rerun: `uv run pytest tests/ -v`
