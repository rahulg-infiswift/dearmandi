from pydantic import BaseModel, EmailStr, SecretStr, Field, ConfigDict, BeforeValidator
from typing import Annotated, Optional
from datetime import datetime, timezone

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(UserBase):
    password: SecretStr

class UserCreateDB(UserBase):
    hashed_password: str
    is_verified: bool = False

class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    password: Optional[SecretStr] = None

class UserInDB(UserBase):
    id: PyObjectId = Field(alias="_id")
    hashed_password: str
    is_verified: bool = False

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

class UserPublic(UserBase):
    id: PyObjectId = Field(alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
