from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.article import Article
from app.models.favorite import Favorite


def toggle_favorite(db: Session, user_id: int, article_id: int) -> tuple[Article | None, bool]:
    """Toggle favorite status. Returns (article, is_now_favorited)."""
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        return None, False

    existing = (
        db.query(Favorite)
        .filter(Favorite.user_id == user_id, Favorite.article_id == article_id)
        .first()
    )
    if existing:
        db.delete(existing)
        db.commit()
        return article, False
    else:
        fav = Favorite(user_id=user_id, article_id=article_id)
        db.add(fav)
        db.commit()
        return article, True


def is_favorited(db: Session, user_id: int, article_id: int) -> bool:
    return (
        db.query(Favorite)
        .filter(Favorite.user_id == user_id, Favorite.article_id == article_id)
        .first()
        is not None
    )


def get_favorite_count(db: Session, article_id: int) -> int:
    return db.query(func.count(Favorite.id)).filter(Favorite.article_id == article_id).scalar() or 0


def get_user_favorite_ids(db: Session, user_id: int) -> set[int]:
    rows = db.query(Favorite.article_id).filter(Favorite.user_id == user_id).all()
    return {r[0] for r in rows}


def get_favorite_counts(db: Session, article_ids: list[int]) -> dict[int, int]:
    """Get favorite counts for a batch of articles. Returns {article_id: count}."""
    if not article_ids:
        return {}
    rows = (
        db.query(Favorite.article_id, func.count(Favorite.id))
        .filter(Favorite.article_id.in_(article_ids))
        .group_by(Favorite.article_id)
        .all()
    )
    return {article_id: count for article_id, count in rows}


def list_favorites(db: Session, user_id: int) -> list[Article]:
    return (
        db.query(Article)
        .join(Favorite, Favorite.article_id == Article.id)
        .options(joinedload(Article.author), joinedload(Article.tags))
        .filter(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .all()
    )
