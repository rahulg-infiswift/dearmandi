import os
from fastapi import Depends, HTTPException
import motor.motor_asyncio
from .config import settings

# Create a new client and connect to the server
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)

async def check_mongodb_connection():
    try:
        # Send a ping command to the server to check if MongoDB is available
        await client.admin.command('ping')
        print("MongoDB connected.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Could not connect to MongoDB")

# Function to close the MongoDB connection
async def close_mongodb_connection():
    print("Closing MongoDB connection")
    client.close()


# Database connection
def get_db():
    db = client.get_database(settings.DATABASE)
    return db

# Dependency to get the user collection
async def get_user_collection(db=Depends(get_db)):
    return db.get_collection("users")

# Dependency to get the todo collection
async def get_todo_collection(db=Depends(get_db)):
    return db.get_collection("todos")