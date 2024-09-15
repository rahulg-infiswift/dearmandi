from pydantic import BaseModel, EmailStr, SecretStr

class User(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr | None = None

class UserInDB(User):
    hashed_password: str
    is_verified: bool = False

class SignUpUser(User):
    password: SecretStr