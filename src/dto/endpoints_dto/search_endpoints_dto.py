from pydantic import BaseModel

from src.dto.spotify_dto import Track


class SearchDTO(BaseModel):
    tracks: list[Track]