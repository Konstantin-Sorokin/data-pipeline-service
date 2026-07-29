import httpx


class BaseApiClient:
    def __init__(self, client: httpx.AsyncClient, base_url: str):
        self._client = client
        self._base_url = base_url.rstrip("/")

    async def _request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        """Выполнить HTTP-запрос к API."""
        url = f"{self._base_url}/{endpoint.lstrip('/')}"

        return await self._client.request(method, url, **kwargs)

    async def get(self, endpoint: str, **kwargs) -> httpx.Response:
        """Выполнить GET-запрос к API."""
        return await self._request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> httpx.Response:
        """Выполнить POST-запрос к API."""
        return await self._request("POST", endpoint, **kwargs)
