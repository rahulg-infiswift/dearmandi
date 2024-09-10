from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routes import users, todos
from .controllers import todo_controller
from .database import (
    check_mongodb_connection,
    close_mongodb_connection,
)

from dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_mongodb_connection()
    yield
    await close_mongodb_connection()


app = FastAPI(lifespan=lifespan)

app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(todos.router, prefix="/api/todo", tags=["Todo"])


@app.get("/")
async def read_root():
    return {"Hello": "Dearmandi"}


