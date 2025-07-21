from fastapi.security import OAuth2PasswordBearer
from core.config import settings
from fastapi import Depends,HTTPException,status
from models.user_models import User
from jose import jwt, JWTError,ExpiredSignatureError
from  schemas.auth_schemas import TokenPayload
from datetime import datetime
from pydantic import ValidationError
from services.user_service import UserService
token_reusavel = OAuth2PasswordBearer(
    tokenUrl= f"{settings.API_V1_STR}/auth/login",
    scheme_name="JWT"

)
async def get_current_user(token: str = Depends(token_reusavel)) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Erro na validacao do token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Payload invalido",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = await UserService.get_user_by_id(token_data.sub)  # busca o usuário no banco pelo ID no token
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Não foi possível encontrar o usuário',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return user  # retorna o objeto do usuário, que corresponde ao UserDetail esperado
