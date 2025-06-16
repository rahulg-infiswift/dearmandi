from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from typing import List

from ..database import get_commodity_collection
from ..schemas.commodity_schema import (
    CommodityCreate,
    CommodityUpdate,
    CommodityInDB,
)
from .auth import get_current_verified_user

router = APIRouter()

@router.post("/", response_model=CommodityInDB)
async def create_commodity(
    commodity: CommodityCreate,
    current_user=Depends(get_current_verified_user),
    commodity_collection=Depends(get_commodity_collection),
):
    print("Posting commodity:", commodity)
    
    existing_commodity = await commodity_collection.find_one({
        "name": commodity.name,
        "owner_id": current_user.id,
    })
    if existing_commodity:
        raise HTTPException(status_code=400, detail="Commodity already registered for this user")

    # Convert commodity to dict and add owner_id
    commodity_dict = commodity.model_dump()
    commodity_dict["owner_id"] = current_user.id  # Associate with current user
    result = await commodity_collection.insert_one(commodity_dict)

    # Fetch the newly created commodity to include the generated '_id'
    new_commodity = await commodity_collection.find_one({"_id": result.inserted_id})
    return CommodityInDB(**new_commodity)

@router.get("", response_model=List[CommodityInDB])
async def list_commodities(
    current_user=Depends(get_current_verified_user),
    commodity_collection=Depends(get_commodity_collection),
):
    print("Fetching commodities for user:", current_user.id)
    print("User details:", current_user)

    commodities_cursor = commodity_collection.find({
        "owner_id": current_user.id,
    })
    commodities = await commodities_cursor.to_list(length=None)
    return [CommodityInDB(**commodity) for commodity in commodities]

@router.get("/{commodity_id}", response_model=CommodityInDB)
async def get_commodity(
    commodity_id: str,
    current_user=Depends(get_current_verified_user),
    commodity_collection=Depends(get_commodity_collection),
):
    if not ObjectId.is_valid(commodity_id):
        raise HTTPException(status_code=400, detail="Invalid commodity ID")
    commodity = await commodity_collection.find_one({
        "_id": ObjectId(commodity_id),
        "owner_id": current_user.id,
    })
    if commodity:
        return CommodityInDB(**commodity)
    raise HTTPException(status_code=404, detail="Commodity not found")

@router.put("/{commodity_id}", response_model=CommodityInDB)
async def update_commodity(
    commodity_id: str,
    commodity: CommodityUpdate,
    current_user=Depends(get_current_verified_user),
    commodity_collection=Depends(get_commodity_collection),
):
    if not ObjectId.is_valid(commodity_id):
        raise HTTPException(status_code=400, detail="Invalid commodity ID")
    update_result = await commodity_collection.update_one(
        {
            "_id": ObjectId(commodity_id),
            "owner_id": current_user.id,
        },
        {"$set": commodity.model_dump(exclude_unset=True, exclude="owner_id")}
    )
    if update_result.modified_count == 1:
        updated_commodity = await commodity_collection.find_one({"_id": ObjectId(commodity_id)})
        return CommodityInDB(**updated_commodity)
    elif update_result.matched_count == 1:
        existing_commodity = await commodity_collection.find_one({"_id": ObjectId(commodity_id)})
        return CommodityInDB(**existing_commodity)
    else:
        raise HTTPException(status_code=404, detail="Commodity not found or not owned by user")

@router.delete("/{commodity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_commodity(
    commodity_id: str,
    current_user=Depends(get_current_verified_user),
    commodity_collection=Depends(get_commodity_collection),
):
    print("Deleting commodity:", commodity_id)

    if not ObjectId.is_valid(commodity_id):
        raise HTTPException(status_code=400, detail="Invalid commodity ID")
    
    delete_result = await commodity_collection.delete_one({
        "_id": ObjectId(commodity_id),
        "owner_id": current_user.id
    })
    if delete_result.deleted_count == 1:
        return  # Successfully deleted, return 204 No Content
    else:
        raise HTTPException(status_code=404, detail="Commodity not found")
