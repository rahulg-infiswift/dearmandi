
from typing import List
from fastapi import APIRouter, HTTPException

from ..schemas import todo_schema

from ..controllers import todo_controller


router = APIRouter()

@router.get("/", response_model=List[todo_schema.Todo])
async def get_todo():
    response = await todo_controller.fetch_all_todos()
    return response

@router.get("/{title}", response_model=List[todo_schema.Todo])
async def get_todo_by_title(title):
    response = await todo_controller.fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {title}")

@router.post("/", response_model=todo_schema.Todo)
async def post_todo(todo: todo_schema.Todo):
    response = await todo_controller.create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@router.put("/{title}", response_model=todo_schema.Todo)
async def put_todo(title: str, desc: str):
    response = await todo_controller.update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {title}")

@router.delete("/{title}")
async def delete_todo(title):
    response = await todo_controller.remove_todo(title)
    if response:
        return "Successfully deleted todo"
    raise HTTPException(404, f"There is no todo with the title {title}")

