from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from .auth import get_current_verified_user, get_password_hash
from ..schemas.user_schema import UserPublic, UserInDB, UserUpdate
from ..database import get_user_collection

router = APIRouter(tags=["Users"])

@router.get("/me", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[UserInDB, Depends(get_current_verified_user)]
):
    """
    Retrieve the current authenticated user's public information.
    """
    return UserPublic(**current_user.model_dump())

@router.put("/me", response_model=UserPublic)
async def update_user_me(
    user_update: UserUpdate,
    current_user: Annotated[UserInDB, Depends(get_current_verified_user)],
    user_collection=Depends(get_user_collection),
):
    """
    Update the current authenticated user's information.
    """
    update_data = user_update.model_dump(exclude_unset=True)
    if 'password' in update_data:
        # Hash the new password
        hashed_password = get_password_hash(update_data.pop('password').get_secret_value())
        update_data['hashed_password'] = hashed_password
    if update_data:
        await user_collection.update_one(
            {"_id": current_user.id},
            {"$set": update_data}
        )
    # Fetch the updated user
    updated_user = await user_collection.find_one({"_id": current_user.id})
    return UserPublic(**updated_user)

@router.get("/me/items/", response_model=list)
async def read_own_items(
    current_user: Annotated[UserInDB, Depends(get_current_verified_user)],
):
    """
    Retrieve items owned by the current authenticated user.
    """
    # Placeholder for user's items. Replace with actual logic to retrieve items.
    return [{"item_id": "Foo", "owner": current_user.email}]
