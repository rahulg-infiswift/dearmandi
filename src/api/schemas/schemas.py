from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class CreateCustomer(BaseModel):
    name: str
    email: EmailStr

class GetCustomer(BaseModel):
    id: int
    name: str

class UserLogin(BaseModel):
    username: EmailStr
    password: str

class GetAccount(BaseModel):
    id: int
    name: str
    description: str | None
    

class CreateTaxAccountsSchema(BaseModel):
    customer_id : int

class CreateTransactionSchema(BaseModel):
    customer_id: int
    amount: int

class CreateCashPurchaseSchema(BaseModel):
    customer_name: str
    crop_name: str
    quantity: int
    amount: int

class CreateCashSaleSchema(BaseModel):
    customer_name: str
    crop_name: str
    quantity: int
    amount: int