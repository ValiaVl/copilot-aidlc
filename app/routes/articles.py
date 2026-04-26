import bleach
import markdown
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.routes.auth import get_current_user, require_auth
from app.services.article_service import (
    create_article,
    get_article,
    list_articles,
    toggle_stale,
    update_article,
)
from app.templating import templates

router = APIRouter()

ALLOWED_TAGS = [
    "a", "abbr", "acronym", "b", "blockquote", "br", "code", "div",
    "em", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "img",
    "li", "ol", "p", "pre", "span", "strong", "table", "tbody",
    "td", "th", "thead", "tr", "ul",
]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "img": ["src", "alt", "title"],
    "td": ["align"],
    "th": ["align"],
}


def render_markdown(text: str) -> str:
    html = markdown.markdown(text, extensions=["tables", "fenced_code"])
    return bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)


@router.get("/", name="home")
def home(
    request: Request,
    tag: str | None = None,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if user is None:
        return RedirectResponse(url="/signin", status_code=303)
    articles = list_articles(db, tag=tag)
    return templates.TemplateResponse(
        request,
        "articles/list.html",
        context={
            "articles": articles,
            "current_tag": tag,
            "user": user,
        },
    )


@router.get("/articles/new", name="article_new")
def get_create_form(
    request: Request,
    user=Depends(require_auth),
):
    return templates.TemplateResponse(
        request,
        "articles/form.html",
        context={
            "user": user,
            "article": None,
            "errors": {},
            "tag_values": [""],
        },
    )


@router.post("/articles", name="article_create")
def post_create(
    request: Request,
    title: str = Form(""),
    body: str = Form(""),
    tags: list[str] = Form([]),
    user=Depends(require_auth),
    db: Session = Depends(get_db),
):
    errors = {}
    title = title.strip()
    if not title:
        errors["title"] = "Title is required"
    elif len(title) > 200:
        errors["title"] = "Title must be 200 characters or fewer"
    if not body.strip():
        errors["body"] = "Body is required"
    elif len(body) > 50_000:
        errors["body"] = "Body must be 50,000 characters or fewer"

    if errors:
        return templates.TemplateResponse(
            request,
            "articles/form.html",
            context={
                "user": user,
                "article": None,
                "errors": errors,
                "title_value": title,
                "body_value": body,
                "tag_values": tags or [""],
            },
            status_code=422,
        )

    clean_tags = [t.strip().lower() for t in tags if t.strip()]
    article = create_article(db, title, body, clean_tags, user.id)
    return RedirectResponse(url=f"/articles/{article.id}", status_code=303)


@router.get("/articles/{article_id}", name="article_detail")
def get_article_detail(
    request: Request,
    article_id: int,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if user is None:
        return RedirectResponse(url="/signin", status_code=303)
    article = get_article(db, article_id)
    if article is None:
        return HTMLResponse("Article not found", status_code=404)
    rendered_body = render_markdown(article.body)
    return templates.TemplateResponse(
        request,
        "articles/detail.html",
        context={
            "user": user,
            "article": article,
            "rendered_body": rendered_body,
        },
    )


@router.get("/articles/{article_id}/edit", name="article_edit")
def get_edit_form(
    request: Request,
    article_id: int,
    user=Depends(require_auth),
    db: Session = Depends(get_db),
):
    article = get_article(db, article_id)
    if article is None:
        return HTMLResponse("Article not found", status_code=404)
    tag_values = [t.name for t in article.tags] or [""]
    return templates.TemplateResponse(
        request,
        "articles/form.html",
        context={
            "user": user,
            "article": article,
            "errors": {},
            "title_value": article.title,
            "body_value": article.body,
            "tag_values": tag_values,
        },
    )


@router.post("/articles/{article_id}/edit", name="article_update")
def post_edit(
    request: Request,
    article_id: int,
    title: str = Form(""),
    body: str = Form(""),
    tags: list[str] = Form([]),
    user=Depends(require_auth),
    db: Session = Depends(get_db),
):
    errors = {}
    title = title.strip()
    if not title:
        errors["title"] = "Title is required"
    elif len(title) > 200:
        errors["title"] = "Title must be 200 characters or fewer"
    if not body.strip():
        errors["body"] = "Body is required"
    elif len(body) > 50_000:
        errors["body"] = "Body must be 50,000 characters or fewer"

    if errors:
        article = get_article(db, article_id)
        return templates.TemplateResponse(
            request,
            "articles/form.html",
            context={
                "user": user,
                "article": article,
                "errors": errors,
                "title_value": title,
                "body_value": body,
                "tag_values": tags or [""],
            },
            status_code=422,
        )

    clean_tags = [t.strip().lower() for t in tags if t.strip()]
    update_article(db, article_id, title, body, clean_tags, user.id)
    return RedirectResponse(url=f"/articles/{article_id}", status_code=303)


@router.post("/articles/{article_id}/stale", name="article_toggle_stale")
def post_toggle_stale(
    request: Request,
    article_id: int,
    user=Depends(require_auth),
    db: Session = Depends(get_db),
):
    article = toggle_stale(db, article_id)
    if article is None:
        return HTMLResponse("Article not found", status_code=404)
    return templates.TemplateResponse(
        request,
        "partials/stale_banner.html",
        context={"article": article},
    )


@router.post("/articles/preview", name="article_preview")
def post_preview(
    request: Request,
    body: str = Form(""),
    user=Depends(require_auth),
):
    rendered = render_markdown(body)
    return templates.TemplateResponse(
        request,
        "partials/preview.html",
        context={"rendered_body": rendered},
    )


@router.get("/articles/tag-field", name="tag_field")
def get_tag_field(request: Request):
    return templates.TemplateResponse(
        request,
        "partials/tag_field.html",
        context={"value": ""},    )