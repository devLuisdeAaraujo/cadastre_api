from fastapi import APIRouter, Depends,HTTPException,status,Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from services.user_service import UserService
from core.security import create_refresh_token,create_acess_token
from schemas.auth_schemas import TokenSchema
from schemas.user_schemas import UserDetail
from models.user_models import User
from api.api_v1.dependecies.user_deps import get_current_user
from pydantic import ValidationError
from core.config import settings
from schemas.auth_schemas import TokenPayload
from jose import jwt

auth_router =APIRouter()

@auth_router.post('/login',summary='Cria Acess Token e Refresh Token',response_model=TokenSchema)
async def login(data:OAuth2PasswordRequestForm = Depends())->Any:
    usuario = await UserService.authenticate(
        email=data.username,
        password = data.password
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='E-mail ou Senha estao incorretos'
        )
    #Criar acess_token
    return {
        "access_token":create_acess_token(usuario.user_id),
        "refresh_token":create_refresh_token(usuario.user_id)
    }


    
@auth_router.post("/token_teste",summary='Testanto token',response_model=UserDetail)
async def teste_token(user:User = Depends(get_current_user)):
    return user

@auth_router.post("/refresh_token",summary='Cria um novo refresh token',response_model=TokenSchema)
async def refresh_token(refresh_token:str= Body(...)):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Payload invalido",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Não foi possível encontrar o usuário',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    return {
        "access_token": create_acess_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id)
    }