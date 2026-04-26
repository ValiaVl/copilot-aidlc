from sqlalchemy.orm import Session, joinedload

from app.models.article import Article
from app.models.tag import Tag


def search(
    db: Session,
    query: str | None = None,
    tag: str | None = None,
) -> list[Article]:
    q = db.query(Article).options(
        joinedload(Article.author), joinedload(Article.tags)
    )

    if tag:
        q = q.join(Article.tags).filter(Tag.name == tag.strip().lower())

    if query:
        pattern = f"%{query.strip()}%"
        q = q.filter(
            Article.title.ilike(pattern) | Article.body.ilike(pattern)
        )

    return q.order_by(Article.updated_at.desc()).all()
