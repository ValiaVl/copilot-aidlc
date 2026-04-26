from pathlib import Path

from fastapi.templating import Jinja2Templates

_templates_dir = Path(__file__).parent / "templates"

templates = Jinja2Templates(directory=str(_templates_dir))
# Disable LRU cache to avoid Python 3.14 hashability issue with dict context
templates.env.cache = {}
