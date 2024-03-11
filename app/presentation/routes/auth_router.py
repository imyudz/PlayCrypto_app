from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.domain.models.dao.user import User
from utils.auth_utils import authenticate_user, get_user_token
from dependencies.auth_dependencies import get_current_active_user
from domain.schemas.response_schemas.auth_response_schema import CurrentUserResponseModel as __CurrentUserResponseModel, TokenResponseModel as __TokenResponseModel, _TokenResponse
from domain.schemas.request_schemas.auth_request_schema import UserRequest
from usecases.user_usecase import create_auth_user


auth_router = APIRouter(tags=["Authentication Routes"])

@auth_router.get("/users/actual", response_model=__CurrentUserResponseModel, name="read-current-user")
async def read_current_user(current_user: User = Depends(get_current_active_user)) -> __CurrentUserResponseModel:
    """Get the authenticated user"""
    return __CurrentUserResponseModel(status=status.HTTP_200_OK, results=current_user.model_dump())

@auth_router.post("/users/create", name="create-user", response_model=__TokenResponseModel)
async def users_create(user: UserRequest) -> __TokenResponseModel:
    try: 
        auth_token: _TokenResponse = create_auth_user(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return __TokenResponseModel(status=status.HTTP_201_CREATED, results=auth_token)

@auth_router.post("/token", response_model=__TokenResponseModel)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> __TokenResponseModel:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token: _TokenResponse = get_user_token(user)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error generating user token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return __TokenResponseModel(status=status.HTTP_200_OK, results=access_token)