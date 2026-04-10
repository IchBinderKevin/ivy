from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator

from models.attachment_model import AttachmentModel
from models.location_model import LocationModel
from models.tag_model import TagModel


class ItemResponseModel(BaseModel):
    """
    Model representing the response data for an item, including all relevant details and associations.
    """
    id: int
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    location: Optional[LocationModel] = None
    tags: list[TagModel] = []
    quantity: int = 1
    isbn: Optional[str] = None
    notes: Optional[str] = None
    date_of_purchase: Optional[datetime] = Field(serialization_alias="dateOfPurchase", default=None)
    buy_price: Optional[float] = Field(serialization_alias="buyPrice", default=None)
    bought_from: Optional[str] = Field(serialization_alias="boughtFrom", default=None)
    model_number: Optional[str] = Field(serialization_alias="modelNumber", default=None)
    serial_number: Optional[str] = Field(serialization_alias="serialNumber", default=None)
    attachments: list[str] = []

    @field_validator("attachments", mode="before")
    @classmethod
    def extract_paths(cls, v):
        return [a.attachment_path if hasattr(a, "attachment_path") else a for a in v]

    class Config:
        from_attributes = True
        populate_by_name = True

class ItemModel(BaseModel):
    """
    Model representing the data required to create an item.
    """
    id: Optional[int] = None
    name: str
    description: str
    image: Optional[str] = None
    location: Optional[LocationModel] = None
    location_id: Optional[int] = None
    attachments: Optional[list[AttachmentModel]] = []
    created_at: datetime = datetime.now()
    tags: list[TagModel] = []
    tag_ids: list[int] = []
    date_of_purchase: Optional[datetime] = Field(alias="dateOfPurchase", default=None)
    buy_price: Optional[float] = Field(alias="buyPrice", default=None)
    bought_from: Optional[str] = Field(alias="boughtFrom", default=None)
    isbn: Optional[str] = None
    model_number: Optional[str] = Field(alias="modelNumber", default=None)
    notes: Optional[str] = None
    quantity: int = 1
    serial_number: Optional[str] = Field(alias="serialNumber", default=None)
