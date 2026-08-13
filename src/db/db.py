import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "toaster"

client = AsyncIOMotorClient(MONGO_URI, maxPoolSize=100, minPoolSize=10)
db = client[DB_NAME]

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
    
    client.close()
    print("MongoDB connection pool cleanly closed.")