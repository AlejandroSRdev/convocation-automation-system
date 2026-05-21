from sqlalchemy import Boolean, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class PlayerModel(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    number: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    category_badge: Mapped[str | None] = mapped_column(String, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
