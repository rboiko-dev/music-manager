from pydantic import BaseModel
from src.dto.spotify_dto import Track


class TracksData(BaseModel):
    href: str
    next: str
    limit: int
    total: int
    items: list[Track]


class SearchTracksRequest(BaseModel):
    tracks: TracksData
