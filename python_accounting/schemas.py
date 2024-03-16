from pydantic import BaseModel

class CreateEntitySchema(BaseModel):
    name: str

class CreateAccountsSchema(BaseModel):
    entity_id : int

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