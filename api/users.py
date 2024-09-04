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
    prefix="/api/users",
    tags=["Users"] 
)

@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=schemas.GetUser)
def create_user(payload: schemas.CreateUser):
    print(payload)
    with get_session(engine) as session:
        # Check if the user already exists in the database
        db_user = session.query(models.User).filter(models.User.email == payload.email).first()
        print(db_user)
        if db_user:
            raise HTTPException(status_code=400, detail="user already exists")
            
        # Hash the password
        hashed_password = utils.get_password_hash(payload.password)
        payload.password = hashed_password

        # If the user does not exist, create a new one
        user = models.User(**payload.model_dump())
        session.add(user)
        session.commit() # This automatically sets up a Reporting Period for the user

        currency = models.Currency(name="US Dollars", code="USD", user_id=user.id)
        session.add(currency)
        session.commit()
        session.refresh(user)

        return user
    
@router.get("/", response_model=List[schemas.GetUser])
def get_users():
    with get_session(engine) as session:
        stmt = select(models.User)
        users = session.scalars(stmt).all()
        return users


@router.get("/{user_id}", response_model=schemas.GetUser)
def get_user(user_id: int):
    with get_session(engine) as session:
        user = session.query(models.User).filter(models.User.id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail=f"User with id: {id} does not exist")
        
        return user
    
