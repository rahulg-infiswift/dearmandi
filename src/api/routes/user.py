from typing import Annotated
from fastapi import APIRouter, Depends

from .auth import get_current_active_user
from ..schemas.user_schema import User, UserInDB

router = APIRouter(tags=["Users"])

# Protected route example
@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@router.get("/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
