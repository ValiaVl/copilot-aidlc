from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EditLog(Base):
    __tablename__ = "edit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id", ondelete="CASCADE"), nullable=False
    )
    editor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    edited_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    article = relationship("Article", back_populates="edit_logs")
    editor = relationship("User", back_populates="edits")
