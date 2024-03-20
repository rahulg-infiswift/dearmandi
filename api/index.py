from datetime import datetime
import json
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from python_accounting.config import config
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import and_, select

from python_accounting.models import Base
from sqlalchemy import create_engine
from python_accounting.database.session import get_session
from python_accounting import models, schemas, transactions
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

@app.get("/api/entities")
def list_entities():
    with get_session(engine) as session:
        stmt = select(models.Entity)
        entities = session.scalars(stmt).all()
        return entities
    
@app.get("/api/entities/{entity_id}")
def list_entity(entity_id: int):
    with get_session(engine) as session:
        entity = session.query(models.Entity).filter(models.Entity.id == entity_id).first()
        return entity

@app.post("/api/create-entity")
def create_entity(payload: schemas.CreateEntitySchema):
    print("Hello there!")
    print(payload)
    with get_session(engine) as session:
        # Check if the entity already exists in the database
        db_entity = session.query(models.Entity).filter(models.Entity.name == payload.name).first()
        print(db_entity)
        if db_entity:
            raise HTTPException(status_code=400, detail="Entity already exists")
            
        # If the entity does not exist, create a new one
        entity = models.Entity(name=payload.name)
        session.add(entity)
        session.commit() # This automatically sets up a Reporting Period for the Entity

        currency = models.Currency(name="US Dollars", code="USD", entity_id=entity.id)
        session.add(currency)
        session.commit()
        return {"id": entity.id, "name": entity.name}

@app.get("/api/get-accounts/{entity_id}")
def list_accounts(entity_id):
    with get_session(engine) as session:
        entity = session.query(models.Entity).filter(models.Entity.id == entity_id).first()
        session.entity = entity
        accounts = session.query(models.Account).all()
        return accounts

@app.post("/api/create-accounts")
def create_accounts(payload: schemas.CreateAccountsSchema):
    print("Create account payload", payload)
    with get_session(engine) as session:
        entity = session.query(models.Entity).filter(models.Entity.id == payload.entity_id).first()
        session.entity = entity
        currency = session.query(models.Currency).filter(models.Currency.entity_id == payload.entity_id).first()
        # Setup Accounts
        tax_account = models.Account(
            name="Tax Account",
            account_type= models.Account.AccountType.CONTROL,
            currency_id=currency.id,
            entity_id=entity.id,
        )
        bank_account = models.Account(
            name="Bank Account",
            account_type=models.Account.AccountType.BANK,
            currency_id=currency.id,
            entity_id=entity.id,
        )
        revenue_account = models.Account(
            name="Revenue Account",
            account_type=models.Account.AccountType.OPERATING_REVENUE,
            currency_id=currency.id,
            entity_id=entity.id,
        )
        client_account = models.Account(
            name="Client Account",
            account_type=models.Account.AccountType.RECEIVABLE,
            currency_id=currency.id,
            entity_id=entity.id,
        )
        supplier_account = models.Account(
            name="Supplier Account",
            account_type=models.Account.AccountType.PAYABLE,
            currency_id=currency.id,
            entity_id=entity.id,
        )
        opex_account = models.Account(
            name="Opex Account",
            account_type=models.Account.AccountType.OPERATING_EXPENSE,
            currency_id=currency.id,
            entity_id=entity.id,
        )
        expense_account = models.Account(
            name="Expense Account",
            account_type=models.Account.AccountType.DIRECT_EXPENSE,
            currency_id=currency.id,
            entity_id=entity.id,
        )
        asset_account = models.Account(
            name="Asset Account",
            account_type=models.Account.AccountType.NON_CURRENT_ASSET,
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

@app.post("/api/create-tax-accounts")
def create_tax_accounts(payload: schemas.CreateTaxAccountsSchema):
    with get_session(engine) as session:
        entity = session.query(models.Entity).filter(models.Entity.id == payload.entity_id).first()
        session.entity = entity
        tax_account = session.query(models.Account).filter(
            and_(models.Account.entity_id == payload.entity_id,
                 models.Account.name == "Tax Account")
        ).first()

        output_tax = models.Tax(
            name="Output Vat",
            code="OTPT",
            account_id=tax_account.id, # This account was created earlier
            rate=20,
            entity_id=entity.id,
        )
        input_tax = models.Tax(
            name="Input Vat",
            code="INPT",
            account_id=tax_account.id,
            rate=10,
            entity_id=entity.id,
        )
        session.add_all([output_tax, input_tax])
        session.commit()

@app.post("/api/create-cash-purchase")   
def transaction(payload: schemas.CreateCashPurchaseSchema):
    print("hello there!")
    with get_session(engine) as session:
        entity = session.query(models.Entity).filter(models.Entity.name == payload.entity_name).first()
        session.entity = entity
        print("entity_id", entity.id)
        bank_account = session.query(models.Account).filter(
            and_(models.Account.entity_id == entity.id,
                 models.Account.name == "Bank Account")
        ).first()
        opex_account = session.query(models.Account).filter(
            and_(models.Account.entity_id == entity.id,
                 models.Account.name == "Opex Account")
        ).first()
        output_tax = session.query(models.Tax).filter(
            and_(models.Tax.entity_id == entity.id,
                 models.Tax.name == "Output Vat")
        ).first()

        print("bank_account", bank_account)
        cash_purchase = transactions.CashPurchase(
            narration="Cash Purchase Transaction",
            transaction_date=datetime.now(),
            account_id=bank_account.id,
            entity_id=entity.id,
        )
        session.add(cash_purchase)
        session.flush()
        cash_purchase_line_item = models.LineItem(
            narration=payload.crop_name,
            account_id=opex_account.id,
            amount=payload.amount,
            quantity= payload.quantity,
            tax_id=output_tax.id,
            entity_id=entity.id,
        )
        session.add(cash_purchase_line_item)
        session.flush()

        cash_purchase.line_items.add(cash_purchase_line_item)
        session.add(cash_purchase)
        cash_purchase.post(session)

@app.post("/api/create-cash-sale")   
def transaction(payload: schemas.CreateCashSaleSchema):
    print("hello there!")
    with get_session(engine) as session:
        entity = session.query(models.Entity).filter(models.Entity.name == payload.entity_name).first()
        session.entity = entity
        print("entity_id", entity.id)
        bank_account = session.query(models.Account).filter(
            and_(models.Account.entity_id == entity.id,
                 models.Account.name == "Bank Account")
        ).first()
        revenue_account = session.query(models.Account).filter(
            and_(models.Account.entity_id == entity.id,
                 models.Account.name == "Revenue Account")
        ).first()
        output_tax = session.query(models.Tax).filter(
            and_(models.Tax.entity_id == entity.id,
                 models.Tax.name == "Output Vat")
        ).first()

        print("bank_account", bank_account)
        cash_sale = transactions.CashSale(
            narration="Cash Sale Transaction",
            transaction_date=datetime.now(),
            account_id=bank_account.id,
            entity_id=entity.id,
        )
        session.add(cash_sale)
        session.flush() # Intermediate save does not record the transaction in the Ledger

        cash_sale_line_item = models.LineItem(
            narration="Cash Sale line item",
            account_id=revenue_account.id,
            amount=100,
            tax_id=output_tax.id,
            entity_id=entity.id,
        )
        session.add(cash_sale_line_item)
        session.flush()

        cash_sale.line_items.add(cash_sale_line_item)
        session.add(cash_sale)
        cash_sale.post(session) # This posts the Transaction to the Ledger

@app.get("/api/income-statement/{entity_id}")
def income_statement(entity_id: int):
    with get_session(engine) as session:
        entity = session.query(models.Entity).filter(models.Entity.id == entity_id).first()
        session.entity = entity

        income_statement = IncomeStatement(session) 
        income_statement_str = str(income_statement)
        print(income_statement)
        return {"income_statement" : income_statement_str}

if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)
