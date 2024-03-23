from datetime import datetime, timedelta, timezone
from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from sqlalchemy import and_, select
from sqlalchemy import create_engine

from python_accounting.models import Base
from python_accounting.database.session import get_session
from python_accounting import models, schemas, transactions
from python_accounting.reports import IncomeStatement
from python_accounting.config import config
from api import utils
database = config.database
engine = create_engine(database["url"])
Base.metadata.create_all(engine) # run migrations to create tables

from  . import token, users, accounts

app = FastAPI()
app.include_router(token.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(utils.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/create_cash_purchase")   
def transaction(payload: schemas.CreateCashPurchaseSchema, ):
    print("hello there!")
    with get_session(engine) as session:
        user = session.query(models.User).filter(models.User.name == payload.user_name).first()
        session.user = user
        print("user_id", user.id)
        bank_account = session.query(models.Account).filter(
            and_(models.Account.user_id == user.id,
                 models.Account.name == "Bank Account")
        ).first()
        opex_account = session.query(models.Account).filter(
            and_(models.Account.user_id == user.id,
                 models.Account.name == "Opex Account")
        ).first()
        output_tax = session.query(models.Tax).filter(
            and_(models.Tax.user_id == user.id,
                 models.Tax.name == "Output Vat")
        ).first()

        print("bank_account", bank_account)
        cash_purchase = transactions.CashPurchase(
            narration="Cash Purchase Transaction",
            transaction_date=datetime.now(),
            account_id=bank_account.id,
            user_id=user.id,
        )
        session.add(cash_purchase)
        session.flush()
        cash_purchase_line_item = models.LineItem(
            narration=payload.crop_name,
            account_id=opex_account.id,
            amount=payload.amount,
            quantity= payload.quantity,
            tax_id=output_tax.id,
            user_id=user.id,
        )
        session.add(cash_purchase_line_item)
        session.flush()

        cash_purchase.line_items.add(cash_purchase_line_item)
        session.add(cash_purchase)
        cash_purchase.post(session)

@app.post("/api/create_cash_sale")   
def transaction(payload: schemas.CreateCashSaleSchema):
    print("hello there!")
    with get_session(engine) as session:
        user = session.query(models.User).filter(models.User.name == payload.user_name).first()
        session.user = user
        print("user_id", user.id)
        bank_account = session.query(models.Account).filter(
            and_(models.Account.user_id == user.id,
                 models.Account.name == "Bank Account")
        ).first()
        revenue_account = session.query(models.Account).filter(
            and_(models.Account.user_id == user.id,
                 models.Account.name == "Revenue Account")
        ).first()
        output_tax = session.query(models.Tax).filter(
            and_(models.Tax.user_id == user.id,
                 models.Tax.name == "Output Vat")
        ).first()

        print("bank_account", bank_account)
        cash_sale = transactions.CashSale(
            narration="Cash Sale Transaction",
            transaction_date=datetime.now(),
            account_id=bank_account.id,
            user_id=user.id,
        )
        session.add(cash_sale)
        session.flush() # Intermediate save does not record the transaction in the Ledger

        cash_sale_line_item = models.LineItem(
            narration="Cash Sale line item",
            account_id=revenue_account.id,
            amount=100,
            tax_id=output_tax.id,
            user_id=user.id,
        )
        session.add(cash_sale_line_item)
        session.flush()

        cash_sale.line_items.add(cash_sale_line_item)
        session.add(cash_sale)
        cash_sale.post(session) # This posts the Transaction to the Ledger

@app.get("/api/income_statement/{user_id}")
def income_statement(user_id: int):
    with get_session(engine) as session:
        user = session.query(models.User).filter(models.User.id == user_id).first()
        session.user = user

        income_statement = IncomeStatement(session) 
        income_statement_str = str(income_statement)
        print(income_statement)
        return {"income_statement" : income_statement_str}

if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)
