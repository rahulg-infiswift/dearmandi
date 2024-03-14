from datetime import datetime
import json
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from python_accounting.config import config
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import and_, select

from python_accounting.models import Base
from sqlalchemy import create_engine
from python_accounting.database.session import get_session
from python_accounting.models import Account, Entity, Currency, Tax, LineItem
from python_accounting.schemas import CreateEntitySchema, CreateAccountsSchema, CreateTaxAccountsSchema, CreateTransactionSchema
from python_accounting.transactions import CashSale
from python_accounting.reports import IncomeStatement

# url = "postgresql://postgres:ashoktraders@localhost:5432/dearmandi-dev"
# config = config.Config("api/config.toml")
database = config.database
engine = create_engine(database["url"])
Base.metadata.create_all(engine) # run migrations to create tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

@app.get("/api/list_entities")
def list_entities():
    with get_session(engine) as session:
        stmt = select(Entity)
        entities = session.scalars(stmt).all()
        return entities
    
@app.get("/api/list_entities/{entity_id}")
def list_entity(entity_id: int):
    with get_session(engine) as session:
        entity = session.query(Entity).filter(Entity.id == entity_id).first()
        return entity

@app.post("/api/create_entity")
def create_entity(payload: CreateEntitySchema):
    print("Hello there!")
    print(payload)
    with get_session(engine) as session:
        entity = Entity(name=payload.name)
        session.add(entity)
        session.commit() # This automatically sets up a Reporting Period for the Entity

        currency = Currency(name="US Dollars", code="USD", entity_id=entity.id)
        session.add(currency)
        session.commit()

@app.get("/api/list_accounts/{entity_id}")
def list_accounts(entity_id):
    with get_session(engine) as session:
        entity = session.query(Entity).filter(Entity.id == entity_id).first()
        session.entity = entity
        accounts = session.query(Account).all()
        return accounts

@app.post("/api/create_accounts")
def create_accounts(payload: CreateAccountsSchema):
    with get_session(engine) as session:
        entity = session.query(Entity).filter(Entity.id == payload.entity_id).first()
        session.entity = entity
        currency = session.query(Currency).filter(Currency.entity_id == payload.entity_id).first()
        # Setup Accounts
        tax_account = Account(
            name="Tax Account",
            account_type=Account.AccountType.CONTROL,
            currency_id=currency.id,
            entity_id=entity.id,
        )
        bank_account = Account(
            name="Bank Account",
            account_type=Account.AccountType.BANK,
            currency_id=currency.id,
            entity_id=entity.id,
        )
        revenue_account = Account(
            name="Revenue Account",
            account_type=Account.AccountType.OPERATING_REVENUE,
            currency_id=currency.id,
            entity_id=entity.id,
        )
        client_account = Account(
            name="Client Account",
            account_type=Account.AccountType.RECEIVABLE,
            currency_id=currency.id,
            entity_id=entity.id,
        )
        supplier_account = Account(
            name="Supplier Account",
            account_type=Account.AccountType.PAYABLE,
            currency_id=currency.id,
            entity_id=entity.id,
        )
        opex_account = Account(
            name="Opex Account",
            account_type=Account.AccountType.OPERATING_EXPENSE,
            currency_id=currency.id,
            entity_id=entity.id,
        )
        expense_account = Account(
            name="Expense Account",
            account_type=Account.AccountType.DIRECT_EXPENSE,
            currency_id=currency.id,
            entity_id=entity.id,
        )
        asset_account = Account(
            name="Asset Account",
            account_type=Account.AccountType.NON_CURRENT_ASSET,
            currency_id=currency.id,
            entity_id=entity.id,
        )    

        session.add_all([
            tax_account, 
            bank_account, 
            revenue_account, 
            client_account, 
            supplier_account, 
            opex_account, 
            expense_account,  
            asset_account
        ])
        session.commit()

@app.post("/api/create_tax_accounts")
def create_tax_accounts(payload: CreateTaxAccountsSchema):
    with get_session(engine) as session:
        entity = session.query(Entity).filter(Entity.id == payload.entity_id).first()
        session.entity = entity
        tax_account = session.query(Account).filter(
            and_(Account.entity_id == payload.entity_id,
                 Account.name == "Tax Account")
        ).first()

        output_tax = Tax(
            name="Output Vat",
            code="OTPT",
            account_id=tax_account.id, # This account was created earlier
            rate=20,
            entity_id=entity.id,
        )
        input_tax = Tax(
            name="Input Vat",
            code="INPT",
            account_id=tax_account.id,
            rate=10,
            entity_id=entity.id,
        )
        session.add_all([output_tax, input_tax])
        session.commit()

@app.post("/api/transaction")   
def transaction(payload: CreateTransactionSchema):
    with get_session(engine) as session:
        entity = session.query(Entity).filter(Entity.id == payload.entity_id).first()
        session.entity = entity
        bank_account = session.query(Account).filter(
            and_(Account.entity_id == payload.entity_id,
                 Account.name == "Bank Account")
        ).first()
        revenue_account = session.query(Account).filter(
            and_(Account.entity_id == payload.entity_id,
                 Account.name == "Revenue Account")
        ).first()
        output_tax = session.query(Tax).filter(
            and_(Tax.entity_id == payload.entity_id,
                 Tax.name == "Output Vat")
        ).first()

        cash_sale = CashSale(
            narration="Cash Sale Transaction",
            transaction_date=datetime.now(),
            account_id=bank_account.id,
            entity_id=entity.id,
        )
        session.add(cash_sale)
        session.flush() # Intermediate save does not record the transaction in the Ledger

        cash_sale_line_item = LineItem(
            narration="Cash Sale line item",
            account_id=revenue_account.id,
            amount=payload.amount,
            tax_id=output_tax.id,
            entity_id=entity.id,
        )
        session.add(cash_sale_line_item)
        session.flush()

        cash_sale.line_items.add(cash_sale_line_item)
        session.add(cash_sale)
        cash_sale.post(session) # This posts the Transaction to the Ledger

@app.get("/api/income_statement/{entity_id}")
def income_statement(entity_id: int):
    with get_session(engine) as session:
        entity = session.query(Entity).filter(Entity.id == entity_id).first()
        session.entity = entity

        income_statement = IncomeStatement(session) 
        income_statement_str = str(income_statement)
        return json.dumps(income_statement_str)

if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)
