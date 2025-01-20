import logging

from config.dev_config import DevConfig as Config
from src.adapters.search.search_adapter import SpotifySearchCore
from src.adapters.search.search_auth_adapter import SearchAuthClient

config = Config()
search_client = SearchAuthClient()
search_core = SpotifySearchCore()


def init_dependencies():
    client = search_client.init_instance(
        client_id=config.SPOTIFY_CLIENT_ID, secret_key=config.SPOTIFY_CLIENT_SECRET)
    print(client)
    search_core.init_instance(client)
    print(search_core.client)