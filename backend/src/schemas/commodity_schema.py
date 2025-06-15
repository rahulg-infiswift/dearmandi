from pydantic import BaseModel, BeforeValidator, ConfigDict, Field
from typing import Annotated, Optional
from datetime import datetime, timezone

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class CommodityBase(BaseModel):
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CommodityCreate(CommodityBase):
    pass

class CommodityUpdate(CommodityBase):
    pass

class CommodityInDB(CommodityBase):
    id: PyObjectId = Field(alias="_id")
    owner_id: PyObjectId = Field(...)  # Add this line

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
