from pydantic import BaseModel
from typing import Optional, Dict

class CGeckoCoinsListResponse(BaseModel): # response for /coins/list
    id: str
    symbol: str
    name: str
    platforms: Optional[Dict[str, str]] = None