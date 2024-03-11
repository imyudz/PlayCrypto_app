from pydantic import BaseModel
from typing import Optional, TypeVar

T = TypeVar('T', BaseModel, None)

class _ApiPaginationInfo(BaseModel):
    count: int
    pages: int
    next: Optional[str]
    prev: Optional[str]
    

class DefaultAPIResponse(BaseModel):
    pagination_info: Optional[_ApiPaginationInfo] = None
    status: int
    results: T
        
