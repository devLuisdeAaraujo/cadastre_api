from fastapi import APIRouter, Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from services.user_service import UserService
from core.security import create_refresh_token,create_acess_token
from schemas.auth_schemas import TokenSchema
from schemas.user_schemas import UserDetail
from models.user_models import User
from api.api_v1.dependecies.user_deps import get_current_user
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
        "acess_token":create_acess_token(usuario.user_id),
        "refresh_token":create_refresh_token(usuario.user_id)
    }


    
@auth_router.post("/token_teste",summary='Testanto token',response_model=UserDetail)
async def teste_token(User:User = Depends(get_current_user)):
    return User
