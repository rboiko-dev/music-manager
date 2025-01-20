from abc import ABC, abstractmethod


class AbstractSearchAuthRepository(ABC):

    @abstractmethod
    async def _get_access_token(self):
        pass

    @abstractmethod
    async def fetch_page(self, url: str):
        pass
