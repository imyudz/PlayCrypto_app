from pydantic import BaseModel
from enum import Enum

class TokenData(BaseModel):
    usermail: str | None = None
    