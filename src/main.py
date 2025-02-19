from fastapi import FastAPI 
from routes import base_route , data_route , nlp_route
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm import LLMProviderFactory
from stores.vectordb import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser
# Initialize FastAPI app
app = FastAPI()


async def initialize_resources():
    config = get_settings()
    app.mongo_client = AsyncIOMotorClient(config.MONGODB_URL)
    app.database = app.mongo_client[config.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(config=config)
    vectordb_provider_factory = VectorDBProviderFactory(config=config)

    # Initialize Generation providers
    app.generation_client = llm_provider_factory.create(provider=config.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=config.GENERATION_MODEL_ID)

    # Initialize Embedding providers
    app.embedding_client = llm_provider_factory.create(provider=config.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=config.EMBEDDING_MODEL_ID, embedding_size=config.EMBEDDING_MODEL_SIZE)

    # Initialize VectorDB providers
    app.vectordb_client = vectordb_provider_factory.create(provider=config.VECTOR_DB_BACKEND)
    app.vectordb_client.connect()


    # Initialize template parser
    app.template_parser = TemplateParser(
        language=config.PRIMARY_LANG
        , default_language=config.DEFAULT_LANG
    )



async def close_resources():
    app.mongo_client.close()
    app.vectordb_client.disconnect()



app.add_event_handler("startup", initialize_resources)
app.add_event_handler("shutdown", close_resources)

# Include routers for API endpoints

app.include_router(base_route.base_router)
app.include_router(data_route.data_router)
app.include_router(nlp_route.nlp_router)
