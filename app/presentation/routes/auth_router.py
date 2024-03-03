import os
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from domain.schemas.response_schemas.auth_response_schema import TokenResponse
from datetime import timedelta
from domain.models.user import User
from utils.auth_utils import authenticate_user, get_user_token
from dependencies.auth_dependencies import get_current_active_user
from domain.schemas.response_schemas.auth_response_schema import UserResponse
from domain.schemas.request_schemas.auth_request_schema import UserRequest
from usecases.user_usecase import create_auth_user


auth_router = APIRouter(tags=["Authentication Routes"])


@auth_router.get("/users/actual", response_model=UserResponse, name="read-current-user")
async def read_current_user(current_user: User = Depends(get_current_active_user)) -> UserResponse:
    """Get the authenticated user"""
    return UserResponse.model_dump(current_user)

@auth_router.post("/users/create", name="create-user", response_model=TokenResponse)
async def users_create(user: UserRequest) -> TokenResponse:
    try: 
        auth_token: TokenResponse = create_auth_user(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return auth_token

@auth_router.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenResponse:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token: TokenResponse = get_user_token(user)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error generating user token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return access_token