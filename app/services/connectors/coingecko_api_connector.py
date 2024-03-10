from config.async_api import AsyncAPI as __AsyncAPI
class CoingeckoAPIConnector: 
    def __init__(self, coingecko_url: str, coingecko_api_key: str) -> None:
        self.async_api = __AsyncAPI(coingecko_url)
        self.__apikey = coingecko_api_key
        
    async def get_coins_list(self, include_platform: bool = False):
        headers = {"Authorization": f"{self.__apikey}"}
        return await self.__api.request("GET", f"/coins/list?include_platform={include_platform}", headers=headers)