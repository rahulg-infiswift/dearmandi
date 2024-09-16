from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from typing import Annotated, Optional
from datetime import datetime, timezone
from enum import Enum

PyObjectId = Annotated[str, BeforeValidator(str)]

class TransactionType(str, Enum):
    SALE = "sale"
    PURCHASE = "purchase"

class TransactionBase(BaseModel):
    commodity_id: PyObjectId
    counterparty_id: PyObjectId  # Reference to the counterparty
    quantity: float
    price: float
    transaction_type: TransactionType
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    commodity_id: Optional[PyObjectId] = None
    counterparty_id: Optional[PyObjectId] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    transaction_type: Optional[TransactionType] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None

class TransactionInDB(TransactionBase):
    id: PyObjectId = Field(alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
