from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from typing import List

from ..database import get_counterparty_collection
from ..schemas.counterparty_schema import (
    CounterpartyCreate,
    CounterpartyUpdate,
    CounterpartyInDB,
)
from .auth import get_current_verified_user

router = APIRouter()

@router.post("/", response_model=CounterpartyInDB)
async def create_counterparty(
    counterparty: CounterpartyCreate,
    current_user=Depends(get_current_verified_user),
    counterparty_collection=Depends(get_counterparty_collection),
):
    # Optional: Check for existing counterparty by name
    existing = await counterparty_collection.find_one({"name": counterparty.name})
    if existing:
        raise HTTPException(status_code=400, detail="Counterparty already exists")

    counterparty_dict = counterparty.model_dump()
    result = await counterparty_collection.insert_one(counterparty_dict)

    # Fetch the newly created counterparty
    new_counterparty = await counterparty_collection.find_one({"_id": result.inserted_id})
    return CounterpartyInDB(**new_counterparty)

@router.get("/", response_model=List[CounterpartyInDB])
async def list_counterparties(
    current_user=Depends(get_current_verified_user),
    counterparty_collection=Depends(get_counterparty_collection),
):
    print("fetching all counterparties")
    cursor = counterparty_collection.find()
    counterparties = await cursor.to_list(length=None)
    return [CounterpartyInDB(**cp) for cp in counterparties]

@router.get("/{counterparty_id}", response_model=CounterpartyInDB)
async def get_counterparty(
    counterparty_id: str,
    current_user=Depends(get_current_verified_user),
    counterparty_collection=Depends(get_counterparty_collection),
):
    if not ObjectId.is_valid(counterparty_id):
        raise HTTPException(status_code=400, detail="Invalid counterparty ID")
    counterparty = await counterparty_collection.find_one({"_id": ObjectId(counterparty_id)})
    if counterparty:
        return CounterpartyInDB(**counterparty)
    else:
        raise HTTPException(status_code=404, detail="Counterparty not found")

@router.put("/{counterparty_id}", response_model=CounterpartyInDB)
async def update_counterparty(
    counterparty_id: str,
    counterparty: CounterpartyUpdate,
    current_user=Depends(get_current_verified_user),
    counterparty_collection=Depends(get_counterparty_collection),
):
    if not ObjectId.is_valid(counterparty_id):
        raise HTTPException(status_code=400, detail="Invalid counterparty ID")
    update_result = await counterparty_collection.update_one(
        {"_id": ObjectId(counterparty_id)},
        {"$set": counterparty.model_dump(exclude_unset=True)}
    )
    if update_result.modified_count == 1:
        updated_counterparty = await counterparty_collection.find_one({"_id": ObjectId(counterparty_id)})
        return CounterpartyInDB(**updated_counterparty)
    elif update_result.matched_count == 1:
        existing_counterparty = await counterparty_collection.find_one({"_id": ObjectId(counterparty_id)})
        return CounterpartyInDB(**existing_counterparty)
    else:
        raise HTTPException(status_code=404, detail="Counterparty not found")

@router.delete("/{counterparty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_counterparty(
    counterparty_id: str,
    current_user=Depends(get_current_verified_user),
    counterparty_collection=Depends(get_counterparty_collection),
):
    if not ObjectId.is_valid(counterparty_id):
        raise HTTPException(status_code=400, detail="Invalid counterparty ID")
    delete_result = await counterparty_collection.delete_one({"_id": ObjectId(counterparty_id)})
    if delete_result.deleted_count == 1:
        return  # Successfully deleted
    else:
        raise HTTPException(status_code=404, detail="Counterparty not found")
