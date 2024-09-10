from pydantic import BaseModel, EmailStr, SecretStr

class User(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

class SignUpUser(User):
    password: SecretStr