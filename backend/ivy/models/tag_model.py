from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class TagModel(BaseModel):
    """
    Model representing a tag that can be associated with items.
    """
    id: Optional[int] = None
    name: str
    color: str
    created_at: Optional[datetime] = datetime.now()

    class Config:
        from_attributes = True

class TagUsageModel(BaseModel):
    """
    Model representing the usage of tags.
    """
    used: int
    unused: int
