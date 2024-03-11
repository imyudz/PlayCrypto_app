from pydantic import BaseModel
from app.domain.models.dao.user import User
from .api_response_schema import DefaultAPIResponse as _DefaultAPIResponse
from typing import Annotated

class _TokenResponse(BaseModel):
    access_token: str
    token_type: str

class _UserResponse(BaseModel):
    id: int
    created_at: str
    first_name: str
    last_name: str
    email: str
    role: str
    is_active_user: bool
    
class TokenResponseModel(_DefaultAPIResponse):
    results: _TokenResponse

class CurrentUserResponseModel(_DefaultAPIResponse):
    results: _UserResponse