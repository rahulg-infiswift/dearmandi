
from typing import List
from fastapi import APIRouter, Depends, HTTPException


from ..schemas.todo_schema import TodoCreate, TodoInDB
from ..database import get_todo_collection

router = APIRouter()

@router.post("/", response_model=TodoInDB)
async def post_todo(
    todo: TodoCreate,
    todo_collection=Depends(get_todo_collection),
):
    result = await todo_collection.insert_one(todo.model_dump())
    
    # Fetch the newly created commodity to include the generated '_id'
    new_todo = await todo_collection.find_one({"_id": result.inserted_id})

    return TodoInDB(**new_todo)

@router.get("", response_model=List[TodoInDB])
async def get_todo(
    todo_collection=Depends(get_todo_collection),
):
    todos = []
    todo_cursor = todo_collection.find({})
    todos = await todo_cursor.to_list(length=None)
    return todos

@router.get("/{title}", response_model=List[TodoInDB])
async def get_todo_by_title(
    title,
    todo_collection=Depends(get_todo_collection),
):
    documents = []
    todo = await todo_collection.find_one({"title": title})
    if todo:
        return TodoInDB(**todo)
    raise HTTPException(status_code=404, detail=f"There is no todo with the title {title}")


@router.put("/{title}", response_model=TodoInDB)
async def put_todo(
    title: str, 
    desc: str,
    todo_collection=Depends(get_todo_collection),
):
    update_result = await todo_collection.update_one(
        {"title": title}, 
        {"$set": {"description": desc}}
    )
    updated_todo = await todo_collection.find_one({"title": title})
    print("updated_todo", updated_todo)
    if updated_todo:
        return updated_todo
    raise HTTPException(status_code=404, detail=f"There is no todo with the title {title}")

@router.delete("/{title}")
async def delete_todo(
    title,
    todo_collection=Depends(get_todo_collection),
):
    deleted_todo = await todo_collection.delete_one({"title": title})
    if delete_todo:
        return "Successfully deleted todo"
    raise HTTPException(status_code=404, detail=f"There is no todo with the title {title}")

