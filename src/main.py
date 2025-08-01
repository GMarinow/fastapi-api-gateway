from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from src.core.config import SETTINGS
from src.core.logger import create_logger

LOGGER = create_logger(logger_name=SETTINGS.SERVICE_NAME)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Handles application startup, shutdown, and database connection.
    """
    db_client: AsyncIOMotorClient = AsyncIOMotorClient(
        SETTINGS.MONGO_CONNECTION_STRING,
        serverSelectionTimeoutMS=1000,
    )
    try:
        await db_client.admin.command("ping")
        LOGGER.info("Database connection successful.")
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        LOGGER.error(f"Failed to connect to the database: {e}")
        raise

    db: AsyncIOMotorDatabase = db_client[SETTINGS.MONGO_DB_NAME]
    document_models: list = []

    try:
        await init_beanie(database=db, document_models=document_models)
        LOGGER.info("Beanie initialized successfully.")
    except Exception as error:
        LOGGER.error(f"Beanie initialization failed: {error}")
        raise

    yield

    LOGGER.info("Shutting down application ...")
    db_client.close()


app = FastAPI(
    title=SETTINGS.SERVICE_NAME,
    openapi_url="/api/v1/openapi.json" if SETTINGS.ENV == "dev" else None,
    docs_url="/docs" if SETTINGS.ENV == "dev" else None,
    redoc_url="/redoc",
    description=SETTINGS.DESCRIPTION,
    version=SETTINGS.APP_VERSION,
    terms_of_service=SETTINGS.TERMS_OF_SERVICE,
    contact={
        "name": "Georgi Marinov",
        "url": "https://github.com/GMarinow/fastapi-api-gateway",
        "email": "georgi.marinow@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=SETTINGS.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health Check"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
