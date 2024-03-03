import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated
import domain.models.token as token_model
from domain.models.user import User
from jose import JWTError, jwt
from services.repositories.user_repository import SupabaseUserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.environ.get("JWT_SECRET")
ALGORITHM = os.environ.get("ALGORITHM")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):                    
    credentials_exception = HTTPException(                    
        status_code=status.HTTP_401_UNAUTHORIZED,                 
        detail="Could not validade credentials",                  
        headers={"WWW-Authenticate": "Bearer"},                   
    )                 
    try:                  
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])                   
        useremail: str = payload.get("sub")                    
        if useremail is None:                  
            raise credentials_exception                   
        token_data = token_model.TokenData(usermail=useremail)                 
    except JWTError:                  
        raise credentials_exception                   
    user = SupabaseUserRepository().get_user_by_email(email=token_data.usermail)                  
    if user is None:                  
        raise credentials_exception                   
    return user      
           
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.is_active_user is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user