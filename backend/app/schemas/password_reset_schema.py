from pydantic import BaseModel, EmailStr, SecretStr

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: SecretStr
