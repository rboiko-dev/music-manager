from abc import ABC, abstractmethod


class AbstractSearchRepository(ABC):

    @abstractmethod
    async def search(self, query: str, search_type: str):
        pass

    @abstractmethod
    async def artist_details(self, artist_id: str):
        pass

    @abstractmethod
    async def album_details(self, album_id: str):
        pass
