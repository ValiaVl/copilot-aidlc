# Services — Team Knowledge Base

## Service Layer Overview

The service layer sits between routes and models. Routes handle HTTP concerns (request parsing, response rendering). Services handle business logic and database operations.

---

## UserService (`app/services/user_service.py`)

**Responsibility**: User identity management (trust-based)

| Operation | Description |
|-----------|-------------|
| Get or create user | Look up by name (case-insensitive). If not found, create. Return user. |
| Get user by ID | Fetch user for session validation |

**Orchestration**: Called by `auth.py` routes during sign-in. Session middleware stores `user_id` in cookie.

---

## ArticleService (`app/services/article_service.py`)

**Responsibility**: Article lifecycle — create, read, update, stale flagging, edit logging

| Operation | Description |
|-----------|-------------|
| Create article | Insert article + resolve/create tags + link via ArticleTag |
| Get article | Fetch article with joined tags, author, and edit log |
| Update article | Update fields, sync tags (add new, remove old), insert EditLog entry |
| List articles | Fetch all articles (newest first), optionally filter by tag |
| Toggle stale | Flip `is_stale` boolean on article |
| Get edit log | Fetch edit history with editor names, ordered most recent first |

**Orchestration**: Called by `articles.py` routes. Tag resolution (find-or-create by name) is internal to this service.

---

## SearchService (`app/services/search_service.py`)

**Responsibility**: Combined text search + tag filtering

| Operation | Description |
|-----------|-------------|
| Search | Query articles by text (LIKE on title + body) AND/OR tag filter. Return matching articles ordered by relevance/recency. |

**Orchestration**: Called by `search.py` route. Returns article list for HTMX partial rendering. Debounced on the client side via HTMX `hx-trigger="keyup changed delay:300ms"`.
