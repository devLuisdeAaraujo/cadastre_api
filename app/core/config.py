from typing import List
from decouple import config
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
 


class Settings(BaseSettings):
    API_V1_STR : str= "/api/v1"
    JWT_SECRET_KEY : str =  config("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY :str = config("JWT_REFRESH_SECRET_KEY",cast=str)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTE :int =60
    REFRESH_TOKEN_EXPIRE_MINUTES : int = 60*24*7
    BACKEND_CORS_ORIGINS : List[AnyHttpUrl] = []
    PROJECT_NAME : str = "TODO_PROJECT"
    MONGO_CONNECTION_STRING: str  = config("MONGO_CONNECTION_STRING",cast=str)

class COnfig:
    case_sensitive = True


settings = Settings()
