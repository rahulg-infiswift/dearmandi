from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from typing import List

from ..database import (
    get_transaction_collection,
    get_commodity_collection,
    get_counterparty_collection,
)
from ..schemas.transaction_schema import (
    TransactionCreate,
    TransactionUpdate,
    TransactionInDB,
)
from .auth import get_current_verified_user
from ..schemas.transaction_schema import TransactionType

router = APIRouter()

@router.post("/", response_model=TransactionInDB)
async def create_transaction(
    transaction: TransactionCreate,
    current_user=Depends(get_current_verified_user),
    transaction_collection=Depends(get_transaction_collection),
    commodity_collection=Depends(get_commodity_collection),
    counterparty_collection=Depends(get_counterparty_collection),
):
    print("Creating transaction", transaction)
    # Validate commodity_id
    if not ObjectId.is_valid(transaction.commodity_id):
        raise HTTPException(status_code=400, detail="Invalid commodity ID")
    commodity = await commodity_collection.find_one({
        "_id": ObjectId(transaction.commodity_id),
        "owner_id": current_user.id,
    })
    if not commodity:
        raise HTTPException(status_code=404, detail="Commodity not found or not owned by user")

    # Validate counterparty_id
    if not ObjectId.is_valid(transaction.counterparty_id):
        raise HTTPException(status_code=400, detail="Invalid counterparty ID")
    counterparty = await counterparty_collection.find_one({
        "_id": ObjectId(transaction.counterparty_id),
        "owner_id": current_user.id,
    })
    if not counterparty:
        raise HTTPException(status_code=404, detail="Counterparty not found or not owned by user")

    # Optional: Validate counterparty role
    # For example, ensure the counterparty has the appropriate role
    # if transaction.transaction_type == TransactionType.SALE and 'customer' not in counterparty.get('roles', []):
    #     raise HTTPException(status_code=400, detail="Counterparty is not a customer")
    # elif transaction.transaction_type == TransactionType.PURCHASE and 'supplier' not in counterparty.get('roles', []):
    #     raise HTTPException(status_code=400, detail="Counterparty is not a supplier")

    transaction_dict = transaction.model_dump()
    transaction_dict["owner_id"] = current_user.id  # Associate with current user
    result = await transaction_collection.insert_one(transaction_dict)

    # Fetch the newly created transaction
    new_transaction = await transaction_collection.find_one({"_id": result.inserted_id})
    return TransactionInDB(**new_transaction)

@router.get("", response_model=List[TransactionInDB])
async def list_transactions(
    current_user=Depends(get_current_verified_user),
    transaction_collection=Depends(get_transaction_collection),
):
    print(f"Fetching transactions for user: {current_user.id}")
    transactions_cursor = transaction_collection.find({
        "owner_id": current_user.id,
    })
    transactions = await transactions_cursor.to_list(length=None)
    return [TransactionInDB(**transaction) for transaction in transactions]

@router.get("/{transaction_id}", response_model=TransactionInDB)
async def get_transaction(
    transaction_id: str,
    current_user=Depends(get_current_verified_user),
    transaction_collection=Depends(get_transaction_collection),
):
    if not ObjectId.is_valid(transaction_id):
        raise HTTPException(status_code=400, detail="Invalid transaction ID")
    transaction = await transaction_collection.find_one({
        "_id": ObjectId(transaction_id),
        "owner_id": current_user.id,
    })
    if transaction:
        return TransactionInDB(**transaction)
    else:
        raise HTTPException(status_code=404, detail="Transaction not found or not owned by user")

@router.put("/{transaction_id}", response_model=TransactionInDB)
async def update_transaction(
    transaction_id: str,
    transaction: TransactionUpdate,
    current_user=Depends(get_current_verified_user),
    transaction_collection=Depends(get_transaction_collection),
    commodity_collection=Depends(get_commodity_collection),
    counterparty_collection=Depends(get_counterparty_collection),
):
    if not ObjectId.is_valid(transaction_id):
        raise HTTPException(status_code=400, detail="Invalid transaction ID")

    update_data = transaction.model_dump(exclude_unset=True)

    # Validate commodity_id if being updated
    if 'commodity_id' in update_data:
        if not ObjectId.is_valid(update_data['commodity_id']):
            raise HTTPException(status_code=400, detail="Invalid commodity ID")
        commodity = await commodity_collection.find_one({
            "_id": ObjectId(update_data['commodity_id']),
            "owner_id": current_user.id,
        })
        if not commodity:
            raise HTTPException(status_code=404, detail="Commodity not found")

    # Validate counterparty_id if being updated
    if 'counterparty_id' in update_data:
        if not ObjectId.is_valid(update_data['counterparty_id']):
            raise HTTPException(status_code=400, detail="Invalid counterparty ID")
        counterparty = await counterparty_collection.find_one({
            "_id": ObjectId(update_data['counterparty_id']),
            "owner_id": current_user.id,
        })
        if not counterparty:
            raise HTTPException(status_code=404, detail="Counterparty not found")

        # Optional: Validate counterparty role
        # if 'transaction_type' in update_data:
        #     transaction_type = update_data['transaction_type']
        # else:
        #     # Fetch existing transaction to get current transaction_type
        #     existing_transaction = await transaction_collection.find_one({"_id": ObjectId(transaction_id)})
        #     if not existing_transaction:
        #         raise HTTPException(status_code=404, detail="Transaction not found")
        #     transaction_type = existing_transaction['transaction_type']

        # if transaction_type == TransactionType.SALE and 'customer' not in counterparty.get('roles', []):
        #     raise HTTPException(status_code=400, detail="Counterparty is not a customer")
        # elif transaction_type == TransactionType.PURCHASE and 'supplier' not in counterparty.get('roles', []):
        #     raise HTTPException(status_code=400, detail="Counterparty is not a supplier")

    # Validate transaction_type if being updated and counterparty role
    if 'transaction_type' in update_data:
        transaction_type = update_data['transaction_type']
        existing_transaction = await transaction_collection.find_one({"_id": ObjectId(transaction_id)})
        if not existing_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        # Fetch existing counterparty if not already fetched
        if 'counterparty' not in locals():
            counterparty_id = update_data.get('counterparty_id', existing_transaction['counterparty_id'])
            counterparty = await counterparty_collection.find_one({
                "_id": ObjectId(counterparty_id),
                "owner_id": current_user.id
            })
            if not counterparty:
                raise HTTPException(status_code=404, detail="Counterparty not found or not owned by user")

        # Optional: Validate counterparty role based on new transaction_type
        # if transaction_type == TransactionType.SALE and 'customer' not in counterparty.get('roles', []):
        #     raise HTTPException(status_code=400, detail="Counterparty is not a customer")
        # elif transaction_type == TransactionType.PURCHASE and 'supplier' not in counterparty.get('roles', []):
        #     raise HTTPException(status_code=400, detail="Counterparty is not a supplier")

    update_result = await transaction_collection.update_one(
        {
            "_id": ObjectId(transaction_id),
            "owner_id": current_user.id,
        },
        {"$set": update_data}
    )

    if update_result.modified_count == 1:
        updated_transaction = await transaction_collection.find_one({"_id": ObjectId(transaction_id)})
        return TransactionInDB(**updated_transaction)
    elif update_result.matched_count == 1:
        # No changes were made
        existing_transaction = await transaction_collection.find_one({"_id": ObjectId(transaction_id)})
        return TransactionInDB(**existing_transaction)
    else:
        raise HTTPException(status_code=404, detail="Transaction not found or not owned by user")

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: str,
    current_user=Depends(get_current_verified_user),
    transaction_collection=Depends(get_transaction_collection),
):
    if not ObjectId.is_valid(transaction_id):
        raise HTTPException(status_code=400, detail="Invalid transaction ID")
    delete_result = await transaction_collection.delete_one({
        "_id": ObjectId(transaction_id),
        "owner_id": current_user.id,
    })
    if delete_result.deleted_count == 1:
        return  # Successfully deleted
    else:
        raise HTTPException(status_code=404, detail="Transaction not found or not owned by user")
