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
    prefix="/api/customers",
    tags=["Customers"] 
)


@router.post("/create_customer")   
def create_customer(payload: schemas.CreateCustomer, token_user: Annotated[schemas.GetUser, Depends(utils.get_current_user)] ):
    print("customer payload", payload)
    with get_session(engine) as session:
        customer = models.Customer(**payload.model_dump(), user_id=token_user.id)
        session.add(customer)
        session.commit() # This automatically sets up a Reporting Period for the user
        session.refresh(customer)
        return customer



@router.get("/self_customers", response_model=List[schemas.GetCustomer])   
def get_customers(token_user: Annotated[schemas.GetUser, Depends(utils.get_current_user)]):
    with get_session(engine) as session:
        user = session.query(models.User).filter(models.User.id == token_user.id).first()
        session.user = user
        customers = session.query(models.Customer).filter(models.Account.user_id == user.id).all()
        return customers