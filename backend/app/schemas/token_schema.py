from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime

class TokenData(BaseModel):
    email: str | None = None
    expires_at: datetime