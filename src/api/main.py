from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routes import auth, todo, user
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

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(todo.router, prefix="/api/todos", tags=["Todos"])
app.include_router(user.router, prefix="/api/users", tags=["Users"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"Hello": "Dearmandi !!!"}