from models.db_models.base import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column



class ItemAttachment(Base):
    __tablename__ = "item_attachment_mappings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    attachment_path: Mapped[str] = mapped_column(nullable=False)
