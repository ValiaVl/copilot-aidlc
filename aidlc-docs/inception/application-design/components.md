# Components — Team Knowledge Base

## Component Overview

| Component | Module Path | Responsibility |
|-----------|-------------|---------------|
| **Models** | `app/models/` | SQLAlchemy ORM models for User, Article, Tag, ArticleTag, EditLog |
| **Schemas** | `app/schemas/` | Pydantic schemas for request/response validation |
| **Routes** | `app/routes/` | FastAPI route handlers grouped by feature |
| **Services** | `app/services/` | Business logic and database operations |
| **Templates** | `app/templates/` | Jinja2 HTML templates with HTMX attributes |
| **Database** | `app/database.py` | SQLAlchemy engine, session factory, Base |
| **App Entry** | `app/main.py` | FastAPI app creation, middleware, router mounting |

---

## Component Details

### Models (`app/models/`)
- **Purpose**: Define database schema as Python classes
- **Files**: `user.py`, `article.py`, `tag.py`, `edit_log.py`
- **Responsibilities**:
  - Define table structures and relationships
  - Provide ORM mapping for SQLite tables

### Schemas (`app/schemas/`)
- **Purpose**: Validate and shape data for forms and responses
- **Files**: `article.py`, `user.py`
- **Responsibilities**:
  - Validate form input (article creation/editing, sign-in)
  - Shape data for template rendering

### Routes (`app/routes/`)
- **Purpose**: Handle HTTP requests and return HTML responses
- **Files**: `auth.py`, `articles.py`, `search.py`
- **Responsibilities**:
  - `auth.py` — sign-in, sign-out, session management
  - `articles.py` — CRUD, stale flagging, edit history
  - `search.py` — live search endpoint, tag filtering

### Services (`app/services/`)
- **Purpose**: Business logic layer between routes and models
- **Files**: `user_service.py`, `article_service.py`, `search_service.py`
- **Responsibilities**:
  - Encapsulate database queries and business rules
  - Keep routes thin — routes call services, services call models

### Templates (`app/templates/`)
- **Purpose**: Server-rendered HTML with HTMX for dynamic behaviour
- **Layout**: `base.html` (layout), `articles/` (list, detail, form), `auth/` (sign-in), `partials/` (HTMX fragments)
- **Responsibilities**:
  - Render pages with Jinja2
  - HTMX attributes for live search, toggle preview, stale flagging

### Database (`app/database.py`)
- **Purpose**: Database configuration and session management
- **Responsibilities**:
  - Create SQLAlchemy engine for SQLite
  - Provide async session factory
  - Declare Base for ORM models

### App Entry (`app/main.py`)
- **Purpose**: Application bootstrap
- **Responsibilities**:
  - Create FastAPI instance
  - Mount static files and template directories
  - Include route modules
  - Configure session middleware (cookie-based)
  - Run database table creation on startup
