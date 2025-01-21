from fastapi import FastAPI 
from routes import base_route
from routes import data_route

app = FastAPI()

app.include_router(base_route.base_router)
app.include_router(data_route.data_router)

