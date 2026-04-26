from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.routes.auth import get_current_user
from app.services.search_service import search
from app.templating import templates

router = APIRouter()


@router.get("/search", name="search")
def search_articles(
    request: Request,
    q: str | None = Query(None),
    tag: str | None = Query(None),
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    articles = search(db, query=q, tag=tag)
    return templates.TemplateResponse(
        request,
        "partials/article_list.html",
        context={
            "articles": articles,
            "current_tag": tag,
            "user": user,
        },
    )
