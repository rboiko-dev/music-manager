from typing import List
from pydantic import BaseModel


class Image(BaseModel):
    height: int
    width: int
    url: str


class Album(BaseModel):
    id: str
    uri: str
    name: str
    release_date: str
    total_tracks: int
    images: List[Image]


class TrackArtist(BaseModel):
    name: str
    id: str
    uri: str


class Track(BaseModel):
    name: str
    duration_ms: int
    artists: List[TrackArtist]
    album: Album
    uri: str
    id: str


class AlbumTrack(Track):
    album: Album | None = None
    track_number: int


class AlbumDetails(Album):
    tracks: List[AlbumTrack]


class Artist(BaseModel):
    name: str
    id: str
    images: List[Image]
    albums: List[Album]
    top_tracks: List[Track]
