from datetime import datetime, timezone

from sqlalchemy.orm import Session, joinedload

from app.models.article import Article, article_tag
from app.models.edit_log import EditLog
from app.models.tag import Tag


def _resolve_tags(db: Session, tag_names: list[str]) -> list[Tag]:
    tags = []
    for name in tag_names:
        name = name.strip().lower()
        if not name:
            continue
        tag = db.query(Tag).filter(Tag.name == name).first()
        if tag is None:
            tag = Tag(name=name)
            db.add(tag)
            db.flush()
        tags.append(tag)
    return tags


def create_article(
    db: Session,
    title: str,
    body: str,
    tag_names: list[str],
    author_id: int,
) -> Article:
    article = Article(title=title, body=body, author_id=author_id)
    article.tags = _resolve_tags(db, tag_names)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def get_article(db: Session, article_id: int) -> Article | None:
    return (
        db.query(Article)
        .options(
            joinedload(Article.author),
            joinedload(Article.tags),
            joinedload(Article.edit_logs).joinedload(EditLog.editor),
        )
        .filter(Article.id == article_id)
        .first()
    )


def update_article(
    db: Session,
    article_id: int,
    title: str,
    body: str,
    tag_names: list[str],
    editor_id: int,
) -> Article | None:
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        return None

    article.title = title
    article.body = body
    article.updated_at = datetime.now(timezone.utc)
    article.tags = _resolve_tags(db, tag_names)

    edit_log = EditLog(article_id=article.id, editor_id=editor_id)
    db.add(edit_log)
    db.commit()
    db.refresh(article)
    return article


def list_articles(db: Session, tag: str | None = None) -> list[Article]:
    query = db.query(Article).options(
        joinedload(Article.author), joinedload(Article.tags)
    )
    if tag:
        query = query.join(Article.tags).filter(Tag.name == tag.strip().lower())
    return query.order_by(Article.created_at.desc()).all()


def toggle_stale(db: Session, article_id: int) -> Article | None:
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        return None
    article.is_stale = not article.is_stale
    db.commit()
    db.refresh(article)
    return article


def get_edit_log(db: Session, article_id: int) -> list[EditLog]:
    return (
        db.query(EditLog)
        .options(joinedload(EditLog.editor))
        .filter(EditLog.article_id == article_id)
        .order_by(EditLog.edited_at.desc())
        .all()
    )
