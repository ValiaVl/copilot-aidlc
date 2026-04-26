# Component Dependencies — Team Knowledge Base

## Dependency Matrix

| Component | Depends On |
|-----------|-----------|
| `app/main.py` | Routes (auth, articles, search), Database, Templates, Static files |
| `app/routes/auth.py` | UserService, Templates, Session middleware |
| `app/routes/articles.py` | ArticleService, Templates, Session middleware, Markdown renderer |
| `app/routes/search.py` | SearchService, Templates (partials) |
| `app/services/user_service.py` | Models (User), Database session |
| `app/services/article_service.py` | Models (Article, Tag, ArticleTag, EditLog, User), Database session |
| `app/services/search_service.py` | Models (Article, Tag, ArticleTag), Database session |
| `app/models/*` | SQLAlchemy Base from `database.py` |
| `app/templates/*` | HTMX (CDN), CSS (static) |

## Data Flow

```
Browser (HTMX)
    │
    ▼
FastAPI Routes
    │
    ├── auth.py ──────► UserService ──────► User model ──► SQLite
    │
    ├── articles.py ──► ArticleService ──► Article, Tag,
    │                                       ArticleTag,
    │                                       EditLog models ──► SQLite
    │
    └── search.py ────► SearchService ──► Article, Tag
                                          models ──────────► SQLite
    │
    ▼
Jinja2 Templates (HTML + HTMX attributes)
    │
    ▼
Browser renders HTML
```

## Communication Patterns

- **Routes → Services**: Direct function calls (dependency injection via FastAPI `Depends()`)
- **Services → Models**: SQLAlchemy ORM queries via injected database session
- **Routes → Templates**: Jinja2 `TemplateResponse` with context dict
- **Browser → Routes**: Standard HTTP requests + HTMX partial requests (`HX-Request` header)
- **Session**: Cookie-based session middleware storing `user_id`

## HTMX Interaction Patterns

| Interaction | Trigger | Target | Swap |
|-------------|---------|--------|------|
| Live search | `keyup changed delay:300ms` on search input | `#article-list` | `innerHTML` |
| Tag filter | `click` on tag link | `#article-list` | `innerHTML` |
| Toggle stale | `click` on stale button | `#stale-banner` | `outerHTML` |
| Markdown preview | `click` toggle button | `#preview-area` | `innerHTML` |
