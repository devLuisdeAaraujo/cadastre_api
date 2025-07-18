from fastapi import APIRouter, Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from services.user_service import UserService
auth_router =APIRouter()

@auth_router.post('/login')
async def login(data:OAuth2PasswordRequestForm = Depends())->Any:
    usuario = await UserService.authenticate(
        email=data.email,
        password = data.password
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='E-mail ou Senha estao incorretos'
        )
    #Criar acess_token
    
