from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.database import Base, engine
from app.routes import articles, auth, search


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Team Knowledge Base", lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key="knowledgebase-dev-secret-change-in-production",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(articles.router)
app.include_router(search.router)


@app.exception_handler(auth._redirect_to_signin)
def redirect_to_signin(request: Request, exc: auth._redirect_to_signin):
    return RedirectResponse(url="/signin", status_code=303)
