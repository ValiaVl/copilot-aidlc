# Application Design — Team Knowledge Base (Consolidated)

## Project Structure

```
app/
  main.py                  # FastAPI app, middleware, router mounting
  database.py              # SQLAlchemy engine, session, Base
  models/
    user.py                # User model
    article.py             # Article + ArticleTag models
    tag.py                 # Tag model
    edit_log.py            # EditLog model
  schemas/
    article.py             # Article form/response schemas
    user.py                # Sign-in form schema
  routes/
    auth.py                # Sign-in, sign-out
    articles.py            # CRUD, stale flag, preview
    search.py              # Live search + tag filter
  services/
    user_service.py        # User identity (get or create)
    article_service.py     # Article lifecycle, tag sync, edit log
    search_service.py      # Text search + tag filter
  templates/
    base.html              # Layout (nav, HTMX script, CSS)
    auth/
      signin.html          # Sign-in form
    articles/
      list.html            # Article listing (home)
      detail.html          # Article detail + edit log + stale banner
      form.html            # Create/edit form with preview toggle
    partials/
      article_list.html    # HTMX fragment: filtered article cards
      preview.html         # HTMX fragment: rendered markdown
      stale_banner.html    # HTMX fragment: stale warning
  static/
    style.css              # Minimal CSS
```

## Architecture Summary

- **Pattern**: Server-rendered HTML with HTMX for progressive enhancement
- **Layering**: Routes → Services → Models (thin routes, business logic in services)
- **Database**: SQLAlchemy ORM + SQLite (single file)
- **Session**: Cookie-based middleware storing `user_id`
- **Search**: Live search via debounced HTMX requests (`delay:300ms`)
- **Markdown**: Server-side rendering (markdown library)

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| App structure | Modular | Separation of concerns, testable services |
| ORM | SQLAlchemy | Standard Python ORM, well-documented |
| Search UX | Live (debounced) | Better user experience, HTMX makes it simple |
| Tag storage | Separate table + junction | Normalised, supports filtering and reuse |
| Edit tracking | EditLog table | Simple append-only log (who + when) |
| Stale flagging | Boolean on Article | Minimal, toggle via HTMX partial swap |

## Routes Summary

| Method | Path | Purpose | HTMX? |
|--------|------|---------|-------|
| GET | `/signin` | Sign-in page | No |
| POST | `/signin` | Process sign-in | No |
| GET | `/signout` | Sign out | No |
| GET | `/` | Article listing (home) | No |
| GET | `/articles/{id}` | Article detail | No |
| GET | `/articles/new` | Create form | No |
| POST | `/articles` | Create article | No |
| GET | `/articles/{id}/edit` | Edit form | No |
| POST | `/articles/{id}/edit` | Update article | No |
| POST | `/articles/{id}/stale` | Toggle stale | Yes |
| POST | `/articles/preview` | Markdown preview | Yes |
| GET | `/search?q=...&tag=...` | Live search | Yes |

## Data Model

```
User (id, name)
  │
  ├──< Article (id, title, body, author_id, is_stale, created_at, updated_at)
  │       │
  │       ├──< ArticleTag (article_id, tag_id) >── Tag (id, name)
  │       │
  │       └──< EditLog (id, article_id, editor_id, edited_at)
  │
  └──< EditLog (via editor_id)
```

## See Also
- [components.md](components.md) — detailed component responsibilities
- [component-methods.md](component-methods.md) — method signatures and model fields
- [services.md](services.md) — service layer details
- [component-dependency.md](component-dependency.md) — dependency matrix and data flow
