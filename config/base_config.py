import os
from dotenv import load_dotenv

load_dotenv()


class ConfigMeta(type):
    def __call__(cls, *args, **kwargs):
        # here is "before __new__ is called"
        instance = super().__call__(*args, **kwargs)
        # here is "after __new__ and __init__"
        if post_init := getattr(instance, "_check_env_vars", None):
            print(instance)
            post_init()
        return instance


class BaseConfig(metaclass=ConfigMeta):
    def __init__(self):
        self.LOGGING: str = os.getenv('LOGGING', 'DEBUG')

    def _get_required_env(self, var_name: str) -> str:
        self.__dict__.setdefault("_required_vars", set()).add(var_name)
        return os.environ.get(var_name)
