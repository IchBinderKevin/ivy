from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class LocationModel(BaseModel):
    """
    Model representing a location where items can be stored.
    """
    id: Optional[int] = None
    name: str
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True
