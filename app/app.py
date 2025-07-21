from core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from models.user_models import User
from api.api_v1.router import router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
app.add_middleware(
    CORSMiddleware,
    allow_origns = settings.BACKEND_CORS_ORIGINS,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
@app.on_event("startup")
async def app_init():
    client_db = AsyncIOMotorClient(
        settings.MONGO_CONNECTION_STRING
    ).todoapp  
    await init_beanie(
        database=client_db,
        document_models=[
           User
        ]
    )

app.include_router(
    router,
    prefix=settings.API_V1_STR
)
