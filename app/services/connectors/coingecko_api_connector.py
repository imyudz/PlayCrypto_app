from config.async_api import AsyncAPI as _AsyncAPI
class CoingeckoAPIConnector: 
    def __init__(self, coingecko_url: str, coingecko_api_key: str) -> None:
        self._async_api = _AsyncAPI(coingecko_url)
        self.__apikey = coingecko_api_key
        
    async def get_coins_list(self, include_platform: bool = False) -> :
        headers = {"x-cg-demo-api-key": f"{self.__apikey}"}
        return await self._async_api.request("GET", f"/api/v3/coins/list?include_platform={include_platform}", headers=headers)