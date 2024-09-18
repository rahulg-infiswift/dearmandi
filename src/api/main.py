from fastapi import FastAPI
from contextlib import asynccontextmanager

# from fastapi.middleware.cors import CORSMiddleware


from .routes import (
    auth, 
    todo, 
    user, 
    commodity, 
    transaction, 
    counterparty
)
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


app = FastAPI(lifespan=lifespan, redirect_slashes=True)

# CORS Middleware # Not required as using proxy in next.config.js
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods (POST, GET, OPTIONS, etc.)
#     allow_headers=["*"],  # Allow all headers
# )

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(user.router, prefix="/api/users", tags=["Users"])
app.include_router(commodity.router, prefix="/api/commodities", tags=["Commodities"])
app.include_router(transaction.router, prefix="/api/transactions", tags=["Transactions"])
app.include_router(counterparty.router, prefix="/api/counterparties", tags=["Counterparties"])
app.include_router(todo.router, prefix="/api/todos", tags=["Todos"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"Hello": "Dearmandi !!!"}

@app.get("/api", tags=["Root"])
async def read_root():
    return {"Hello": "Python !!!"}