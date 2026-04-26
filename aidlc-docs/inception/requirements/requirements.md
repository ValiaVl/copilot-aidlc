# Requirements Document — Team Knowledge Base

## Intent Analysis

- **User Request**: Build a web app where team members can sign in by name, write markdown documentation articles, tag and search them, edit anyone's articles, and flag outdated ones as stale. Tech stack: FastAPI + HTMX.
- **Request Type**: New Project (greenfield)
- **Scope Estimate**: Multiple Components (backend API, frontend templates, database, search)
- **Complexity Estimate**: Moderate
- **Depth Level**: Standard

---

## Functional Requirements

### FR-1: User Identity (Trust-Based Sign-In)
- Users sign in by entering their display name only — no password, no email
- The system creates or recognises the user by name (case-insensitive match)
- A session cookie keeps the user signed in across page loads
- Users can sign out at any time
- Single-team model: all users share one workspace

### FR-2: Article Authoring
- Any signed-in user can create a new article
- An article consists of: **title**, **markdown body**, **tags** (zero or more), **author name**, **created timestamp**
- Markdown is entered in a text area with a **toggle preview** mode (switch between editing raw markdown and viewing rendered HTML)
- Articles are saved to an **SQLite** database

### FR-3: Article Editing
- Any signed-in user can edit any article (open collaboration model)
- Edits overwrite the current content (no full version history)
- A **simple edit log** records each edit event: editor name + timestamp
- The edit log is visible on the article detail page

### FR-4: Tagging
- Authors (and editors) can assign one or more free-text tags to an article
- Tags are displayed on article cards and the detail page
- Users can click a tag to filter the article list to that tag

### FR-5: Search
- Combined **text search + tag filtering**:
  - Free-text search matches against article title and body
  - Tag filter narrows results to articles with the selected tag(s)
  - Both can be used together
- Search is available from the main article listing page

### FR-6: Stale Flagging
- Any signed-in user can flag an article as **stale**
- Stale articles display a **visual warning banner** but remain fully accessible
- A user can remove the stale flag (un-flag)
- The banner indicates the article may be outdated and should be verified

### FR-7: Article Listing & Navigation
- Home page shows all articles (most recent first)
- Each article card shows: title, author, date, tags, stale indicator (if applicable)
- Clicking an article opens its detail/read view

---

## Non-Functional Requirements

### NFR-1: Tech Stack
- **Backend**: Python 3.12+, FastAPI
- **Frontend**: HTMX for dynamic interactions, server-rendered HTML (Jinja2 templates)
- **Database**: SQLite (single-file, no external DB server)
- **Markdown Rendering**: Server-side (e.g., `markdown` or `markdown-it-py` library)

### NFR-2: Deployment
- Local development only (localhost)
- No containerisation or cloud deployment required at this stage

### NFR-3: Performance
- Acceptable for a small team (< 50 users, < 10 000 articles)
- No caching or optimisation requirements beyond reasonable defaults

### NFR-4: Security
- Trust-based model — no authentication security enforced
- Security extension rules **not enforced** (prototype/internal tool)
- Basic input sanitisation for rendered markdown (prevent XSS in rendered HTML)

### NFR-5: Testing
- Property-based testing **not enforced**
- Standard unit/integration tests as appropriate

---

## Data Model (Conceptual)

| Entity | Key Fields |
|--------|-----------|
| **User** | id, name (unique, case-insensitive) |
| **Article** | id, title, body (markdown), author_id, is_stale, created_at, updated_at |
| **Tag** | id, name (unique, case-insensitive) |
| **ArticleTag** | article_id, tag_id |
| **EditLog** | id, article_id, editor_id, edited_at |

---

## Out of Scope
- Password authentication or OAuth
- Role-based access control
- Full version history / content diffs
- Rich-text (WYSIWYG) editor
- Cloud deployment / Docker
- Email notifications
- API for external consumers (HTMX-driven UI only)
