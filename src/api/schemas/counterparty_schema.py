from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from typing import Annotated, Optional, List
from datetime import datetime, timezone

PyObjectId = Annotated[str, BeforeValidator(str)]

class CounterpartyBase(BaseModel):
    name: str
    contact_info: Optional[str] = None  # Email, phone, etc.
    address: Optional[str] = None
    roles: Optional[List[str]] = []  # e.g., ['customer', 'supplier']
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CounterpartyCreate(CounterpartyBase):
    pass

class CounterpartyUpdate(BaseModel):
    name: Optional[str] = None
    contact_info: Optional[str] = None
    address: Optional[str] = None
    roles: Optional[List[str]] = None
    notes: Optional[str] = None

class CounterpartyInDB(CounterpartyBase):
    id: PyObjectId = Field(alias="_id")
    owner_id: PyObjectId = Field(...)  # Required field to associate with the user

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
