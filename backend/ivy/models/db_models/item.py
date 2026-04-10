from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.db_models.base import Base
from models.db_models.item_attachment_mappings import ItemAttachment
from models.db_models.item_tag import item_tag_mappings
from models.db_models.location import Location
from models.db_models.tag import Tag


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image: Mapped[str] = mapped_column(String, nullable=True)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.id"), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    date_of_purchase: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    buy_price: Mapped[float] = mapped_column(Float, nullable=True)
    bought_from: Mapped[str] = mapped_column(String, nullable=True)
    serial_number: Mapped[str] = mapped_column(String, nullable=True)
    model_number: Mapped[str] = mapped_column(String, nullable=True)
    isbn: Mapped[str] = mapped_column(String, nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    tags: Mapped[list[Tag]] = relationship("Tag", secondary=item_tag_mappings)
    location: Mapped[Location] = relationship("Location")
    attachments: Mapped[list[ItemAttachment]] = relationship("ItemAttachment")
