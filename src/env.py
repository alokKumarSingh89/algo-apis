from decouple import Config, RepositoryEnv
import pathlib 
from functools import lru_cache

BASE_DIR = pathlib.Path(__file__).parent.parent
ENV_PATH = BASE_DIR / ".env"
print(ENV_PATH)

@lru_cache()
def get_config():
    if ENV_PATH.exists():
        return Config(RepositoryEnv(str(ENV_PATH)))
    from decouple import config
    return config

config = get_config()