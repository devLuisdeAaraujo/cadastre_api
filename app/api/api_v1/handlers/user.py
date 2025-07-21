from fastapi import APIRouter, HTTPException, status,Depends
from schemas.user_schemas import UserAuth,UserDetail
from services.user_service import UserService
from pymongo.errors import  DuplicateKeyError
from models.user_models import User
from api.api_v1.dependecies.user_deps import get_current_user


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
    
@user_router.get("/me",summary='Detalhes do Usuario Logado',response_model=UserDetail)
async def get_me(user:User = Depends(get_current_user)):
    return user