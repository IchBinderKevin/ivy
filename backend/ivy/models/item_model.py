from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from models.attachment_model import AttachmentModel
from models.location_model import LocationModel
from models.tag_model import TagModel


class ItemResponseModel(BaseModel):
    """
    Model representing an item / object for response purposes, including already resolved location and tag relations.
    """
    id: int
    name: str
    description: str
    image: Optional[str] = None
    location: Optional[LocationModel] = None
    attachments: Optional[list[str]] = []
    tags: list[TagModel] = []
    date_of_purchase: Optional[datetime] = Field(alias="dateOfPurchase", default=None)
    buy_price: Optional[float] = Field(alias="buyPrice", default=None)
    bought_from: Optional[str] = Field(alias="boughtFrom", default=None)
    isbn: Optional[str] = None
    model_number: Optional[str] = Field(alias="modelNumber", default=None)
    notes: Optional[str] = None
    quantity: int = 1
    serial_number: Optional[str] = Field(alias="serialNumber", default=None)

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

