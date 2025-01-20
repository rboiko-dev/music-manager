from urllib import parse
from dataclasses import dataclass
from typing import Type

from pydantic import ValidationError, TypeAdapter

from src.dto.spotify_dto import Track, AlbumTrack, Album, Artist, AlbumDetails
from src.ports.repositories.search_auth_repository import AbstractSearchAuthRepository
from src.ports.repositories.search_repository import AbstractSearchRepository


@dataclass
class Links:
    search = 'https://api.spotify.com/v1/search'
    artists = 'https://api.spotify.com/v1/artists/'
    albums = 'https://api.spotify.com/v1/albums/'


class SpotifySearchCore(AbstractSearchRepository):
    def __init__(self, client: AbstractSearchAuthRepository | None = None) -> None:
        self.client = client

    def init_instance(self, client: AbstractSearchAuthRepository):
        self.client = client

    @staticmethod
    async def _validate_tracks(
            data: list[dict[str, str]],
            validation_class: Type[Track] | Type[AlbumTrack]
    ) -> list[Track] | list[AlbumTrack]:
        new_data: list[validation_class] = []
        try:
            new_data = TypeAdapter(list[validation_class]).validate_python(data)
        except ValidationError as e:
            raise
        except Exception as e:
            raise

        return new_data

    async def get_artist_albums(self, link: str) -> list[Album]:
        try:
            response = await self.client.fetch_page(link + '/albums')
            collected_data = response['items']
            while response.get('next'):
                response = await self.client.fetch_page(response.get('next'))
                collected_data += response['items']
            return [Album(**album) for album in collected_data]
        except ValidationError as e:
            raise
        except KeyError:
            raise

    async def search(self, query: str, search_type: str = 'track') -> list[Track]:
        # TODO: make multiple algorithms for search_type
        response = await self.client.fetch_page(parse.urljoin(Links.search, f'?q={query}&type={search_type}'))
        tracks = await self._validate_tracks(
            data=response['tracks']['items'], validation_class=Track)
        return tracks

    async def artist_details(self, artist_id: str) -> Artist:
        link = parse.urljoin(Links.artists, artist_id)
        data = await self.client.fetch_page(link)

        top_tracks_data = await self.client.fetch_page(link + '/top-tracks')
        data['top_tracks'] = await self._validate_tracks(
            top_tracks_data['tracks'], validation_class=Track)

        albums = await self.get_artist_albums(link)
        data['albums'] = albums
        return Artist(**data)

    async def album_details(self, album_id) -> AlbumDetails:
        link = parse.urljoin(Links.artists, album_id)
        response = await self.client.fetch_page(link)
        response['tracks'] = await self._validate_tracks(
            response['tracks']['items'], validation_class=AlbumTrack)
        return AlbumDetails(**response)
