# Component Methods — Team Knowledge Base

> **Note**: Method signatures and high-level purpose. Detailed business rules will be defined in Functional Design.

---

## Routes (`app/routes/`)

### auth.py
| Method | Signature | Purpose |
|--------|-----------|---------|
| `get_signin` | `GET /signin` → HTML | Render sign-in page |
| `post_signin` | `POST /signin` (form: name) → Redirect | Create/find user, set session cookie, redirect to home |
| `get_signout` | `GET /signout` → Redirect | Clear session, redirect to sign-in |

### articles.py
| Method | Signature | Purpose |
|--------|-----------|---------|
| `list_articles` | `GET /` → HTML | Render home page with article listing |
| `get_article` | `GET /articles/{id}` → HTML | Render article detail with edit log |
| `get_create_form` | `GET /articles/new` → HTML | Render article creation form |
| `post_create` | `POST /articles` (form: title, body, tags) → Redirect | Create article, redirect to detail |
| `get_edit_form` | `GET /articles/{id}/edit` → HTML | Render article edit form |
| `post_edit` | `POST /articles/{id}/edit` (form: title, body, tags) → Redirect | Update article, log edit, redirect |
| `post_toggle_stale` | `POST /articles/{id}/stale` → HTML partial | Toggle stale flag, return updated banner |
| `get_preview` | `POST /articles/preview` (form: body) → HTML partial | Render markdown preview fragment |

### search.py
| Method | Signature | Purpose |
|--------|-----------|---------|
| `search_articles` | `GET /search?q=...&tag=...` → HTML partial | Live search: return filtered article list fragment |

---

## Services (`app/services/`)

### user_service.py
| Method | Signature | Purpose |
|--------|-----------|---------|
| `get_or_create_user` | `(db, name: str) → User` | Find user by name (case-insensitive) or create new |
| `get_user_by_id` | `(db, user_id: int) → User | None` | Fetch user by ID |

### article_service.py
| Method | Signature | Purpose |
|--------|-----------|---------|
| `create_article` | `(db, title, body, tag_names, author_id) → Article` | Create article with tags |
| `get_article` | `(db, article_id) → Article | None` | Fetch article with tags and edit log |
| `update_article` | `(db, article_id, title, body, tag_names, editor_id) → Article` | Update article, sync tags, log edit |
| `list_articles` | `(db, tag: str | None) → list[Article]` | List articles, optionally filtered by tag |
| `toggle_stale` | `(db, article_id) → Article` | Toggle is_stale flag |
| `get_edit_log` | `(db, article_id) → list[EditLog]` | Fetch edit history for article |

### search_service.py
| Method | Signature | Purpose |
|--------|-----------|---------|
| `search` | `(db, query: str | None, tag: str | None) → list[Article]` | Full-text search + tag filter combined |

---

## Models (`app/models/`)

### user.py — `User`
| Field | Type | Notes |
|-------|------|-------|
| `id` | `Integer, PK` | Auto-increment |
| `name` | `String, unique` | Case-insensitive (stored lowercase) |

### article.py — `Article`
| Field | Type | Notes |
|-------|------|-------|
| `id` | `Integer, PK` | Auto-increment |
| `title` | `String` | Required |
| `body` | `Text` | Markdown content |
| `author_id` | `Integer, FK → User.id` | Creator |
| `is_stale` | `Boolean, default=False` | Stale flag |
| `created_at` | `DateTime` | Auto-set |
| `updated_at` | `DateTime` | Auto-updated |

### tag.py — `Tag`
| Field | Type | Notes |
|-------|------|-------|
| `id` | `Integer, PK` | Auto-increment |
| `name` | `String, unique` | Case-insensitive (stored lowercase) |

### article.py — `ArticleTag` (association)
| Field | Type | Notes |
|-------|------|-------|
| `article_id` | `Integer, FK → Article.id` | Composite PK |
| `tag_id` | `Integer, FK → Tag.id` | Composite PK |

### edit_log.py — `EditLog`
| Field | Type | Notes |
|-------|------|-------|
| `id` | `Integer, PK` | Auto-increment |
| `article_id` | `Integer, FK → Article.id` | Edited article |
| `editor_id` | `Integer, FK → User.id` | Who edited |
| `edited_at` | `DateTime` | Auto-set |
