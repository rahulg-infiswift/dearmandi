from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from ..schemas.user_schema import User, UserInDB, SignUpUser
from ..schemas.token_schema import Token, TokenData
from ..database import get_user_collection

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "0490bdeaed7abb6330a07c0d4e98bbc8f7dfcc142cb08f50aee9dbc26fb7db6c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

router = APIRouter(tags=["Auth"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Get user from mongodb
async def get_user(user_collection, username: str):
    user_dict = await user_collection.find_one({"username": username})
    if user_dict:
        return UserInDB(**user_dict)

async def authenticate_user(user_collection, username: str, password: str):
    user = await get_user(user_collection, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    user_collection=Depends(get_user_collection)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload", payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(user_collection, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return User(**current_user.model_dump())

# Login and generate token
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_collection=Depends(get_user_collection)
) -> Token:
    user = await authenticate_user(user_collection, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# Register new user
@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_user(user: SignUpUser, user_collection=Depends(get_user_collection)):
    existing_user = await user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash the user's password
    hashed_password = get_password_hash(user.password.get_secret_value())
    
    user_dict = user.model_dump(exclude={"password"})
    new_user = UserInDB(**user_dict, hashed_password=hashed_password)
    await user_collection.insert_one(new_user.model_dump())
    return {
        "message": "User registered successfully",
        "user": new_user.model_dump(exclude={"hashed_password"})  # Exclude the hashed_password
    }