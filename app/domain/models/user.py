from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime
from typing import Annotated
import pytz
from enum import Enum


class EnumRoles(Enum):
    ADMIN = "ADMIN"
    USER: str = "USER"

class InsertUserModel(BaseModel):
    last_modified: Annotated[str, Field(alias="last_modified")] = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()
    first_name: Annotated[str, Field(alias="first_name")]
    last_name: Annotated[str, Field(alias="last_name")]
    email: Annotated[EmailStr, Field(alias="email")]
    password_hash: Annotated[str, Field(alias="password_hash")]
    role: Annotated[EnumRoles, Field(alias="role")]
    is_active_user: Annotated[bool, Field(alias="is_active_user")]

    @validator("email")
    def validate_email(cls, v):
        assert "@" in v, "Email inválido"
        return v

class User(InsertUserModel):
    id: Annotated[int, Field(alias="id")]
    created_at: Annotated[str, Field(alias="created_at")]
