from datetime import datetime
import random
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str

class GetUser(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

class UserLogin(BaseModel):
    username: EmailStr
    password: str

class GetAccount(BaseModel):
    id: int
    name: str
    description: str

class CreateTaxAccountsSchema(BaseModel):
    entity_id : int


class CreateTransactionSchema(BaseModel):
    entity_id: int
    amount: int


class CreateCashPurchaseSchema(BaseModel):
    entity_name: str
    crop_name: str
    quantity: int
    amount: int


class CreateCashSaleSchema(BaseModel):
    entity_name: str
    crop_name: str
    quantity: int
    amount: int