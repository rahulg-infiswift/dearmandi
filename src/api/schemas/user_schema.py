from pydantic import BaseModel, EmailStr, SecretStr

class User(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None

class UserInDB(User):
    hashed_password: str
    is_verified: bool = False

class SignUpUser(User):
    password: SecretStr