import os
from fastapi.encoders import jsonable_encoder
from datetime import timedelta
from app.domain.models.dao.user import InsertUserModel, EnumRoles
from domain.schemas.response_schemas.auth_response_schema import TokenResponse
from utils.auth_utils import  encrypt_password, get_user_token
from domain.schemas.request_schemas.auth_request_schema import UserRequest
from services.repositories.user_repository import SupabaseUserRepository

def create_auth_user(user: UserRequest) -> TokenResponse:
    encrypted_pwd = encrypt_password(user.password)
    assert encrypted_pwd != None
    
    try:
        user_insertion = InsertUserModel(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_active_user=True,
            password_hash=encrypted_pwd,
            role=EnumRoles.USER
        )
        
        if SupabaseUserRepository().insert_user(user_insertion):
            return get_user_token(user_insertion)           
            
    except Exception as e:
        raise e
    