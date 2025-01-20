import os

from .base_config import BaseConfig


class DevConfig(BaseConfig):
    def __init__(self):
        self.SPOTIFY_CLIENT_ID = self._get_required_env('SPOTIFY_CLIENT_ID')
        self.SPOTIFY_CLIENT_SECRET = self._get_required_env('SPOTIFY_CLIENT_SECRET')
        super().__init__()
