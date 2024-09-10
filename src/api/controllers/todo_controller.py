import os
from ..schemas.todo_schema import Todo
from ..database import get_todo_collection

collection = get_todo_collection()

async def fetch_one_todo(title):
    documents = []
    cursor = collection.find({"title": title})
    # document = await collection.find_one({"title": title})
    async for document in cursor:
        documents.append(Todo(**document))
    return documents

async def fetch_all_todos():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos

async def create_todo(todo):
    document = todo
    result = await collection.insert_one(document)
    return document


async def update_todo(title, desc):
    await collection.update_one({"title": title}, {"$set": {"description": desc}})
    document = await collection.find_one({"title": title})
    print("document", document)
    return document

async def remove_todo(title):
    await collection.delete_one({"title": title})
    return True