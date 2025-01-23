from fastapi import FastAPI 
from routes import base_route
from routes import data_route
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings


# Initialize FastAPI app
app = FastAPI()

@app.on_event("startup")
async def initialize_resources():
    config = get_settings()
    app.mongo_client = AsyncIOMotorClient(config.MONGO_URL)
    app.database = app.mongo_client[config.MONGO_DATABASE]

@app.on_event("shutdown")
async def close_resources():
    app.mongo_client.close()

    
# Include routers for API endpoints

app.include_router(base_route.base_router)
app.include_router(data_route.data_router)