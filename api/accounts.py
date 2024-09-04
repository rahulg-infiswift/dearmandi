from datetime import datetime, timedelta, timezone
from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

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

router = APIRouter(
    prefix="/api/accounts",
    tags=["Accounts"] 
)

@router.get("/self_accounts", response_model=List[schemas.GetAccount])
async def get_accounts(token_user: Annotated[schemas.GetUser, Depends(utils.get_current_user)] ):
    with get_session(engine) as session:
        user = session.query(models.User).filter(models.User.id == token_user.id).first()
        session.user = user
        accounts = session.query(models.Account).filter(models.Account.user_id == user.id).all()
        return accounts

@router.post("/create_accounts")
def create_accounts(token_user: Annotated[schemas.GetUser, Depends(utils.get_current_user)]):
    with get_session(engine) as session:
        user = session.query(models.User).filter(models.User.id == token_user.id).first()
        session.user = user
        currency = session.query(models.Currency).filter(models.Currency.user_id == user.id).first()
        # Setup Accounts
        tax_account = models.Account(
            name="Tax Account",
            account_type= models.Account.AccountType.CONTROL,
            currency_id=currency.id,
            user_id=user.id,
        )
        bank_account = models.Account(
            name="Bank Account",
            account_type=models.Account.AccountType.BANK,
            currency_id=currency.id,
            user_id=user.id,
        )
        revenue_account = models.Account(
            name="Revenue Account",
            account_type=models.Account.AccountType.OPERATING_REVENUE,
            currency_id=currency.id,
            user_id=user.id,
        )
        client_account = models.Account(
            name="Client Account",
            account_type=models.Account.AccountType.RECEIVABLE,
            currency_id=currency.id,
            user_id=user.id,
        )
        supplier_account = models.Account(
            name="Supplier Account",
            account_type=models.Account.AccountType.PAYABLE,
            currency_id=currency.id,
            user_id=user.id,
        )
        opex_account = models.Account(
            name="Opex Account",
            account_type=models.Account.AccountType.OPERATING_EXPENSE,
            currency_id=currency.id,
            user_id=user.id,
        )
        expense_account = models.Account(
            name="Expense Account",
            account_type=models.Account.AccountType.DIRECT_EXPENSE,
            currency_id=currency.id,
            user_id=user.id,
        )
        asset_account = models.Account(
            name="Asset Account",
            account_type=models.Account.AccountType.NON_CURRENT_ASSET,
            currency_id=currency.id,
            user_id=user.id,
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

        return {"message": "Accounts created successfully"}

@router.post("/create_tax_accounts")
def create_tax_accounts(token_user: Annotated[schemas.GetUser, Depends(utils.get_current_user)]):
    with get_session(engine) as session:
        user = session.query(models.User).filter(models.User.id == token_user.id).first()
        session.user = user
        tax_account = session.query(models.Account).filter(
            and_(models.Account.user_id == user.id,
                 models.Account.name == "Tax Account")
        ).first()

        output_tax = models.Tax(
            name="Output Vat",
            code="OTPT",
            account_id=tax_account.id, # This account was created earlier
            rate=20,
            user_id=user.id,
        )
        input_tax = models.Tax(
            name="Input Vat",
            code="INPT",
            account_id=tax_account.id,
            rate=10,
            user_id=user.id,
        )
        session.add_all([output_tax, input_tax])
        session.commit()
        return {"message": "Tax-accounts created successfully"}
