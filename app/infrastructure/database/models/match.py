import datetime

from sqlalchemy import Date, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class MatchModel(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    home_team: Mapped[str] = mapped_column(String, nullable=False)
    away_team: Mapped[str] = mapped_column(String, nullable=False)
    matchday: Mapped[int] = mapped_column(Integer, nullable=False)
    match_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    match_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    competition_type: Mapped[str] = mapped_column(String, nullable=False)
