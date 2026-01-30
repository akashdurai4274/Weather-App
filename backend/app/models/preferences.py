import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    default_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    default_country: Mapped[str | None] = mapped_column(String(10), nullable=True)
    default_lat: Mapped[str | None] = mapped_column(String(20), nullable=True)
    default_lon: Mapped[str | None] = mapped_column(String(20), nullable=True)
    units: Mapped[str] = mapped_column(String(10), default="metric", nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="preferences")
