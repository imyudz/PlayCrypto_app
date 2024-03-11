from pydantic import BaseModel
from .api_response_schema import DefaultAPIResponse
from typing import Optional, Dict

class CGeckoCoinsListResponse(BaseModel): # response for /coins/list
    id: str
    symbol: str
    name: str
    platforms: Optional[Dict[str, str]] = None

class _CoinResponse(BaseModel):
    id: str
    last_modified: str
    coingecko_id: str
    name: str
    symbol: str

class CoinsListResponseModel(DefaultAPIResponse):
    results: list[_CoinResponse]