from fastapi import APIRouter, HTTPException, status
from schemas.user_schemas import UserAuth,UserDetail
from services.user_service import UserService
from pymongo.errors import  DuplicateKeyError


user_router = APIRouter()

@user_router.post("/add_user",summary='Adicionar Usuario',response_model=UserDetail)
async def inserir_usuario(data:UserAuth):
    try:
        return await UserService.create_user(data)
    
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username ou e-mail deste usuario ja existe'
        )
    
