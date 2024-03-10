from pydantic import BaseModel
from app.domain.models.dao.user import User
from typing import Annotated

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    created_at: str
    first_name: str
    last_name: str
    email: str
    role: str
    is_active_user: bool