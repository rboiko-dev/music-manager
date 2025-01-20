import asyncio
import base64
from datetime import datetime, timedelta
import aiohttp

from src.ports.repositories.search_auth_repository import AbstractSearchAuthRepository


class SearchAuthClient(AbstractSearchAuthRepository):

    def __init__(self, client_id: str = None, secret_key: str = None):
        self._expiration_time: datetime | None = None
        self.client_id: str = client_id
        self.secret_key: str = secret_key
        self.token_link: str = 'https://accounts.spotify.com/api/token'

    def init_instance(self, client_id: str, secret_key: str):
        self.client_id: str = client_id
        self.secret_key: str = secret_key

        return self

    @property
    def is_expired_token(self) -> bool:
        now = datetime.now()
        if not self._expiration_time:
            return True
        return now > self._expiration_time

    async def _get_access_token(self):
        try:
            credentials = f"{self.client_id}:{self.secret_key}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {encoded_credentials}"
            }
            body = {
                "grant_type": "client_credentials",
            }
            async with aiohttp.ClientSession() as session:
                response = await session.post(
                    self.token_link,
                    headers=headers, data=body)

                response_data = await response.json()
                self.access_token = response_data.get('access_token')
                self.expiration_time = datetime.now() + timedelta(hours=1)
                self.headers = {
                    'Authorization': f'Bearer {self.access_token}'
                }
                if not self.access_token:
                    raise ValueError(f'Access token was not updated. Authentication response: {response_data}')
                await session.close()
        except aiohttp.ClientError as e:
            print(f"Error getting token: {e}")
        except asyncio.TimeoutError:
            print(f"Request to {self.token_link} timed out")

    async def fetch_page(self, url: str) -> dict[str:str]:
        if self.is_expired_token:
            await self._get_access_token()
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(url, headers=self.headers)
                result = await response.json()
                await session.close()
                return result
        except aiohttp.ClientError as e:
            pass
        except asyncio.TimeoutError:
            pass



