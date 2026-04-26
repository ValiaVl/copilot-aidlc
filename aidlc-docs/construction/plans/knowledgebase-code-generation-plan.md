# Code Generation Plan — Team Knowledge Base

## Unit Context
- **Unit**: knowledgebase (single unit)
- **Project Type**: Greenfield
- **Workspace Root**: `c:\Users\ValiaVlachopoulou\AI-Trainings\copilot-po-aws`
- **Tech Stack**: Python 3.12+, FastAPI, SQLAlchemy, Jinja2, HTMX, SQLite
- **Stories**: US-1 through US-14

## Target Project Structure

```
app/
  __init__.py
  main.py
  database.py
  models/
    __init__.py
    user.py
    article.py
    tag.py
    edit_log.py
  schemas/
    __init__.py
    article.py
    user.py
  routes/
    __init__.py
    auth.py
    articles.py
    search.py
  services/
    __init__.py
    user_service.py
    article_service.py
    search_service.py
  templates/
    base.html
    auth/
      signin.html
    articles/
      list.html
      detail.html
      form.html
    partials/
      article_list.html
      preview.html
      stale_banner.html
      tag_field.html
  static/
    style.css
tests/
  __init__.py
  conftest.py
  test_user_service.py
  test_article_service.py
  test_search_service.py
  test_routes_auth.py
  test_routes_articles.py
  test_routes_search.py
requirements.txt
README.md
```

## Generation Steps

### Step 1: Project Setup
- [x] Create `requirements.txt` with dependencies (fastapi, uvicorn, sqlalchemy, jinja2, python-multipart, markdown, bleach, itsdangerous, httpx, pytest, pytest-asyncio)
- [x] Create `app/__init__.py`
- [ ] Stories: Foundation for all stories

### Step 2: Database Layer
- [x] Create `app/database.py` — SQLAlchemy engine, session factory, Base
- [ ] Stories: Foundation for all data stories

### Step 3: ORM Models
- [x] Create `app/models/__init__.py` — export all models
- [x] Create `app/models/user.py` — User model
- [x] Create `app/models/article.py` — Article + ArticleTag models
- [x] Create `app/models/tag.py` — Tag model
- [x] Create `app/models/edit_log.py` — EditLog model
- [ ] Stories: US-1, US-3, US-5, US-6, US-7, US-11

### Step 4: Pydantic Schemas
- [x] Create `app/schemas/__init__.py`
- [x] Create `app/schemas/user.py` — SignIn form schema
- [x] Create `app/schemas/article.py` — Article create/edit schemas
- [ ] Stories: US-1, US-3, US-5

### Step 5: Service Layer — UserService
- [x] Create `app/services/__init__.py`
- [x] Create `app/services/user_service.py` — get_or_create_user, get_user_by_id
- [ ] Stories: US-1, US-2

### Step 6: Service Layer — ArticleService
- [x] Create `app/services/article_service.py` — create, get, update, list, toggle_stale, get_edit_log
- [ ] Stories: US-3, US-5, US-6, US-7, US-8, US-11, US-12, US-13

### Step 7: Service Layer — SearchService
- [x] Create `app/services/search_service.py` — combined text + tag search
- [ ] Stories: US-9, US-10

### Step 8: Service Layer Unit Tests
- [x] Create `tests/__init__.py` and `tests/conftest.py` — test DB fixtures
- [x] Create `tests/test_user_service.py`
- [x] Create `tests/test_article_service.py`
- [x] Create `tests/test_search_service.py`
- [ ] Stories: US-1 through US-12

### Step 9: Routes — Auth
- [x] Create `app/routes/__init__.py`
- [x] Create `app/routes/auth.py` — sign-in, sign-out, auth middleware dependency
- [ ] Stories: US-1, US-2

### Step 10: Routes — Articles
- [x] Create `app/routes/articles.py` — CRUD, stale toggle, preview, tag field partial
- [ ] Stories: US-3, US-4, US-5, US-6, US-7, US-11, US-12, US-13, US-14

### Step 11: Routes — Search
- [x] Create `app/routes/search.py` — live search endpoint
- [ ] Stories: US-9, US-10

### Step 12: Route Unit Tests
- [x] Create `tests/test_routes_auth.py`
- [x] Create `tests/test_routes_articles.py`
- [x] Create `tests/test_routes_search.py`
- [ ] Stories: US-1 through US-14

### Step 13: Templates — Layout and Auth
- [x] Create `app/templates/base.html` — layout with nav, HTMX CDN, CSS
- [x] Create `app/templates/auth/signin.html` — sign-in form
- [ ] Stories: US-1, US-2

### Step 14: Templates — Articles
- [x] Create `app/templates/articles/list.html` — article listing with search
- [x] Create `app/templates/articles/detail.html` — article detail, edit log, stale banner
- [x] Create `app/templates/articles/form.html` — create/edit form with preview toggle
- [ ] Stories: US-3, US-4, US-5, US-6, US-7, US-8, US-13, US-14

### Step 15: Templates — HTMX Partials
- [x] Create `app/templates/partials/article_list.html` — article cards fragment
- [x] Create `app/templates/partials/preview.html` — markdown preview fragment
- [x] Create `app/templates/partials/stale_banner.html` — stale banner fragment
- [x] Create `app/templates/partials/tag_field.html` — dynamic tag input field
- [ ] Stories: US-4, US-8, US-9, US-10, US-11, US-12

### Step 16: Static Assets and App Entry
- [x] Create `app/static/style.css` — minimal styling
- [x] Create `app/main.py` — FastAPI app, middleware, router mounting, startup
- [ ] Stories: All

### Step 17: README
- [x] Create `README.md` — project overview, setup, run instructions
- [ ] Stories: Documentation

### Step 18: Code Generation Summary
- [x] Create `aidlc-docs/construction/knowledgebase/code/code-summary.md` — summary of all generated files
