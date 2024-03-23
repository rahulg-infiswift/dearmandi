from datetime import datetime, timedelta, timezone
from typing import Annotated

from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy import create_engine
from python_accounting.database.session import get_session
from python_accounting import models, schemas
from python_accounting.config import config
database = config.database
engine = create_engine(database["url"])

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "1295d17d91f641c3e342426ac7ca3ccf2afdad7ff18f2540e3f0afbea7e09875"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

router = APIRouter(
    prefix="/api/utils",
    tags=["Utils"] 
)

@router.get("/get_current_user", response_model=schemas.GetUser)
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    # get user
    with get_session(engine) as session:
        # Check if the user already exists in the database
        db_user = session.query(models.User).filter(models.User.email == token_data.email).first()
        if db_user is None:
            raise credentials_exception
    print("db_user:", db_user)
    return db_user

