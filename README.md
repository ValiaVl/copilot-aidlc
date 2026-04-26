# Team Knowledge Base

A lightweight internal documentation tool where team members can write, search, and maintain short markdown articles. Built with FastAPI + HTMX.

## Features

- **Trust-based sign-in** — enter your name, no password needed
- **Markdown articles** — write documentation with toggle preview
- **Tagging** — organize articles with free-text tags
- **Live search** — find articles by text and/or tag filter
- **Open editing** — anyone can edit any article, with edit history tracking
- **Stale flagging** — flag outdated articles so others know to verify

## Tech Stack

- **Backend**: Python 3.12+, FastAPI, SQLAlchemy
- **Frontend**: Jinja2 templates, HTMX
- **Database**: SQLite
- **Markdown**: `markdown` + `bleach` for safe rendering

## Quick Start

```bash
# Install dependencies
uv sync

# Run the application
uv run uvicorn app.main:app --reload

# Open in browser
# http://127.0.0.1:8000
```

## Running Tests

```bash
uv run pytest tests/ -v
```

## Project Structure

```
app/
  main.py              # FastAPI app entry point
  database.py          # SQLAlchemy setup
  models/              # ORM models
  schemas/             # Pydantic validation
  routes/              # Route handlers
  services/            # Business logic
  templates/           # Jinja2 + HTMX templates
  static/              # CSS
tests/                 # Unit tests
```
