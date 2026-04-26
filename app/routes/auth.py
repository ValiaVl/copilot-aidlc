from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.user_service import get_or_create_user, get_user_by_id
from app.templating import templates

router = APIRouter()


def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return get_user_by_id(db, user_id)


def require_auth(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if user is None:
        raise _redirect_to_signin()
    return user


class _redirect_to_signin(Exception):
    pass


@router.get("/signin", name="signin")
def get_signin(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(
        request,
        "auth/signin.html",
        context={"error": None},
    )


@router.post("/signin", name="signin_post")
def post_signin(
    request: Request,
    name: str = Form(...),
    db: Session = Depends(get_db),
):
    name = name.strip()
    if not name:
        return templates.TemplateResponse(
            request,
            "auth/signin.html",
            context={"error": "Name is required"},
            status_code=422,
        )

    user = get_or_create_user(db, name)
    request.session["user_id"] = user.id
    request.session["user_name"] = user.name
    return RedirectResponse(url="/", status_code=303)


@router.get("/signout", name="signout")
def get_signout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/signin", status_code=303)
