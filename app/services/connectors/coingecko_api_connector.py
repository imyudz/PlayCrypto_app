from config.async_api import AsyncAPI as _AsyncAPI
from domain.schemas.response_schemas.coin_response_schema import CGeckoCoinsListResponse as _CGeckoCoinsListResponse
class CoingeckoAPIConnector: 
    def __init__(self, coingecko_url: str, coingecko_api_key: str) -> None:
        self._async_api = _AsyncAPI(coingecko_url)
        self.__apikey = coingecko_api_key
        
    async def get_coins_list(self, include_platform: bool = False) -> list[_CGeckoCoinsListResponse]:
        headers = {"x-cg-demo-api-key": f"{self.__apikey}"}
        response = await self._async_api.request("GET", f"/api/v3/coins/list?include_platform={include_platform}", headers=headers)
        print(response.json()[0])
        return [_CGeckoCoinsListResponse(**coin) for coin in response.json()]
