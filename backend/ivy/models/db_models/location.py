from datetime import datetime, UTC
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models.db_models.base import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
