from httpx import AsyncClient as __AsyncClient, Response as __Response
from urllib.parse import urljoin as __urljoin

class AsyncAPI(__AsyncClient):
    def __init__(self, base_url: str | None) -> None:
        self.url = base_url
        super().__init__()
        
    async def request(self, method: str | bytes, url: str | bytes, *args, **kwargs) -> __Response:
        joined_url = __urljoin(self.url, url)
        return await super().request(method, joined_url, *args, **kwargs)