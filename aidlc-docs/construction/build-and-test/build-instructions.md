# Build Instructions — Team Knowledge Base

## Prerequisites
- **Python**: 3.12+
- **uv**: Latest version ([install guide](https://docs.astral.sh/uv/getting-started/installation/))
- **OS**: Windows, macOS, or Linux

## Build Steps

### 1. Install Dependencies
```bash
uv sync
```
This creates a virtual environment and installs all runtime + dev dependencies from `pyproject.toml`.

### 2. Verify Installation
```bash
uv run python -c "import fastapi; import sqlalchemy; import jinja2; print('All dependencies OK')"
```

### 3. Run the Application
```bash
uv run uvicorn app.main:app --reload
```

The app starts at **http://127.0.0.1:8000**. The SQLite database (`knowledgebase.db`) is created automatically on first startup.

### 4. Verify App is Running
- Open http://127.0.0.1:8000 in your browser
- You should see the sign-in page
- Enter any name to sign in

## Environment Details
- **Database**: SQLite file `knowledgebase.db` in project root (auto-created)
- **Session Secret**: Hardcoded dev secret in `app/main.py` (change for production)
- **Static Files**: Served from `app/static/`
- **Templates**: Loaded from `app/templates/`

## Troubleshooting

### uv not found
Install uv: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows) or `curl -LsSf https://astral.sh/uv/install.sh | sh` (Linux/macOS)

### Port 8000 already in use
Use a different port: `uv run uvicorn app.main:app --reload --port 8001`

### Database errors
Delete `knowledgebase.db` and restart the app to recreate the schema.
