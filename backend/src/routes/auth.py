from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from passlib.context import CryptContext

from ..schemas.user_schema import UserCreate, UserInDB, UserPublic, UserCreateDB
from ..schemas.token_schema import Token, TokenData
from ..database import get_user_collection
from ..config import settings

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
# Email Authentication
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER='src/email_templates'
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

router = APIRouter(tags=["Auth"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Get user from mongodb
async def get_user(user_collection, email: str):
    user_dict = await user_collection.find_one({"email": email})
    if user_dict:
        return UserInDB(**user_dict)

async def authenticate_user(user_collection, email: str, password: str) -> UserInDB:
    user = await get_user(user_collection, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    if not user.is_verified:  # Check if the user email is verified
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in"
        )
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    user_collection=Depends(get_user_collection)
) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload", payload)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, expires_at=payload.get("exp"))
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(user_collection, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_verified_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)],
):
    if not current_user.is_verified:
        raise HTTPException(status_code=400, detail="Email not verified")
    return UserInDB(**current_user.model_dump())

# Login and generate token
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_collection=Depends(get_user_collection)
) -> Token:
    # OAuth2PasswordRequestForm expect fields named username and password
    user = await authenticate_user(user_collection, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expires_at = datetime.now(timezone.utc) + access_token_expires
    to_encode={"sub": user.email, "exp": expires_at}
    access_token = create_access_token(to_encode)

    return Token(access_token=access_token, token_type="bearer", expires_at=expires_at)


async def send_verification_email(email: str, token: str):
    verification_link = f"{settings.BASE_URL}/api/auth/verify-email?token={token}"
    message = MessageSchema(
        subject="Verify your Email",
        recipients=[email],  # List of recipients
        template_body={"verification_link": verification_link},  # Using a Jinja template
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="verification_email.html")

@router.get("/verify-email")
async def verify_email(token: str, user_collection=Depends(get_user_collection)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate token",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Verification link has expired")
    except InvalidTokenError:
        raise credentials_exception

    # Find the user in the database and verify them
    user = await user_collection.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Mark the user as verified
    await user_collection.update_one({"email": email}, {"$set": {"is_verified": True}})

    return {"message": "Email verified successfully"}

# Register new user and send verification email
@router.post("/register/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate, 
    user_collection=Depends(get_user_collection)
):
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    # Hash the user's password
    hashed_password = get_password_hash(user.password.get_secret_value())
    
    # Create a new user and store in the database (with is_verified=False initially)
    user_dict = user.model_dump(exclude={"password"})
    new_user = UserCreateDB(**user_dict, hashed_password=hashed_password)
    result = await user_collection.insert_one(new_user.model_dump())
    
    # Fetch the newly created user to include the '_id'
    created_user = await user_collection.find_one({"_id": result.inserted_id})
    user_public = UserPublic(**created_user)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)  # Token valid for 1 hour
    to_encode = {"sub": user_public.email, "exp": expires_at}
    # Create email verification token
    verification_token = create_access_token(to_encode)
    # Send verification email
    await send_verification_email(user.email, verification_token)

    return user_public

