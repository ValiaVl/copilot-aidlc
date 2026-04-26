# Code Generation Plan — Favorites Feature

## Unit Context
- **Feature**: Favorites — mark articles as favorite, "My Favorites" view, toggle from listing + detail pages
- **Requirements**: FR-FAV-1 through FR-FAV-6
- **Existing Codebase**: FastAPI + HTMX knowledge-base app (app/ directory, tests/ directory)
- **Patterns to Follow**: Same as existing stale toggle pattern (HTMX POST → partial swap)

## Files to Create
- `app/models/favorite.py` — Favorite ORM model
- `app/services/favorite_service.py` — Favorite business logic
- `app/templates/partials/favorite_toggle.html` — HTMX partial for heart icon
- `tests/test_favorite_service.py` — Service-layer tests

## Files to Modify
- `app/models/__init__.py` — Export Favorite model
- `app/models/user.py` — Add favorites relationship
- `app/models/article.py` — Add favorites relationship
- `app/routes/articles.py` — Add favorite toggle route, pass favorite data to templates
- `app/templates/partials/article_list.html` — Add heart icon + count to article cards
- `app/templates/articles/detail.html` — Add heart icon + count to detail page
- `app/templates/articles/list.html` — Add "My Favorites" filter toggle
- `app/static/style.css` — Add favorite styling
- `tests/test_routes_articles.py` — Add route tests for favorite toggle

---

## Step-by-Step Plan

### Step 1: Create Favorite Model
- [x] Create `app/models/favorite.py` with Favorite ORM class
  - Fields: id, user_id (FK → users.id), article_id (FK → articles.id), created_at
  - Unique constraint on (user_id, article_id)
  - Relationships back to User and Article
- [x] Modify `app/models/__init__.py` to export Favorite
- [x] Add `favorites` relationship to User model in `app/models/user.py`
- [x] Add `favorites` relationship to Article model in `app/models/article.py`
- **Covers**: FR-FAV-1 (data model)

### Step 2: Create Favorite Service
- [x] Create `app/services/favorite_service.py` with functions:
  - `toggle_favorite(db, user_id, article_id)` → returns (article, is_favorited)
  - `is_favorited(db, user_id, article_id)` → returns bool
  - `get_favorite_count(db, article_id)` → returns int
  - `get_user_favorite_ids(db, user_id)` → returns set of article IDs
  - `list_favorites(db, user_id)` → returns list of Articles, ordered by most recently favorited
- **Covers**: FR-FAV-1, FR-FAV-4, FR-FAV-5

### Step 3: Create Favorite Toggle Partial
- [x] Create `app/templates/partials/favorite_toggle.html`
  - Heart icon: ♥ (filled) when favorited, ♡ (outline) when not
  - HTMX POST to `/articles/{id}/favorite` with `hx-swap="outerHTML"`
  - Show favorites count next to heart
  - data-testid attributes for testing
- **Covers**: FR-FAV-1, FR-FAV-2, FR-FAV-3, FR-FAV-4

### Step 4: Add Favorite Route
- [x] Add `POST /articles/{article_id}/favorite` route in `app/routes/articles.py`
  - Calls `toggle_favorite` service
  - Returns the `favorite_toggle.html` partial (same pattern as stale toggle)
  - Requires authentication
- [x] Import new service functions
- **Covers**: FR-FAV-1

### Step 5: Update Listing Page — Add Favorites to Article Cards
- [x] Modify `app/routes/articles.py` `home()` to pass `favorite_ids` set and `favorite_counts` dict to template
- [x] Modify `app/templates/partials/article_list.html` to include favorite toggle partial in each card
- [x] Modify `app/templates/articles/list.html` to add "My Favorites" filter toggle (button/link that switches between all articles and favorites-only view)
- [x] Add `GET /?favorites=1` support in `home()` route to filter to user's favorites
- **Covers**: FR-FAV-2, FR-FAV-4, FR-FAV-5

### Step 6: Update Detail Page — Add Favorite Toggle
- [x] Modify `app/routes/articles.py` `get_article_detail()` to pass `is_favorited` and `favorite_count` to template
- [x] Modify `app/templates/articles/detail.html` to include favorite toggle partial
- **Covers**: FR-FAV-3, FR-FAV-4

### Step 7: Add CSS Styling
- [x] Add favorite-related styles to `app/static/style.css`:
  - `.favorite-toggle` button styling (borderless, cursor pointer)
  - `.favorite-toggle .heart` styling (color red when filled)
  - `.favorite-count` styling
  - `.favorites-filter` styling for the filter toggle on listing page
- **Covers**: UI polish for all FR-FAV requirements

### Step 8: Write Service Tests
- [x] Create `tests/test_favorite_service.py` with tests:
  - `test_toggle_favorite_on` — favoriting an article
  - `test_toggle_favorite_off` — un-favoriting an article
  - `test_is_favorited` — check favorite status
  - `test_get_favorite_count` — count favorites for an article
  - `test_get_user_favorite_ids` — get all favorite article IDs for a user
  - `test_list_favorites_ordered_by_recent` — verify most-recently-favorited-first ordering
  - `test_favorite_unique_constraint` — verify no duplicate favorites
- **Covers**: FR-FAV-1, FR-FAV-4, FR-FAV-5

### Step 9: Write Route Tests
- [x] Add to `tests/test_routes_articles.py`:
  - `test_toggle_favorite_requires_auth` — 303 redirect when not signed in
  - `test_toggle_favorite_on` — POST to favorite returns heart partial
  - `test_toggle_favorite_off` — POST again toggles off
  - `test_home_shows_favorite_hearts` — article cards include heart icons
  - `test_favorites_filter` — `/?favorites=1` returns only favorited articles
  - `test_detail_shows_favorite_heart` — detail page shows heart
- **Covers**: FR-FAV-1, FR-FAV-2, FR-FAV-3, FR-FAV-5, FR-FAV-6

### Step 10: Verify All Existing Tests Pass
- [x] Run full test suite to confirm no regressions — 54/54 passed
- **Covers**: Quality gate — 39 existing tests + new tests all pass

---

## Story Traceability
| Requirement | Steps |
|------------|-------|
| FR-FAV-1 (Toggle) | 1, 2, 3, 4, 8, 9 |
| FR-FAV-2 (Toggle on listing) | 3, 5, 9 |
| FR-FAV-3 (Toggle on detail) | 3, 6, 9 |
| FR-FAV-4 (Count) | 2, 3, 5, 6, 8 |
| FR-FAV-5 (My Favorites view) | 2, 5, 8, 9 |
| FR-FAV-6 (Signed-in only) | 4, 9 |
