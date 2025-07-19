from fastapi.security import OAuth2PasswordBearer
from core.config import settings
from fastapi import Depends,HTTPException,status
from models.user_models import User
from jose import jwt
from  schemas.auth_schemas import TokenPayload
from datetime import datetime
from pydantic import ValidationError
from services.user_service import UserService
token_reusavel = OAuth2PasswordBearer(
    tokenUrl= f"{settings.API_V1_STR}/auth/login",
    scheme_name="JWT"

)
async def get_current_user(token:str = Depends(token_reusavel)) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            settings.ALGORITHM
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                details='Token foi expirado',
                headers={'WWW-Authenticate':'Bearer'}
            )
    except(jwt.JWTError,ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Erro na validacao do token',
            headers={'WWW-Authenticate':'Bearer'}
        )
    user = await UserService.get_user_by_id(token_data.sub)
    if not User:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            details='Nao foi possivel encontrar o usuario',
            headers={'WWW-Authenticate':'Bearer'}
        )