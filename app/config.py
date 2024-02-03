"""Config."""

from sanic.config import Config
from dotenv import dotenv_values
from functools import lru_cache

DOTENV_FILE = "/hide/.env"

class Dotenv(Config):
    """Config dataclass."""

    LOG_LEVEL: str
    LOG_FORMAT: str
    LOG_FILENAME: str
    LOG_FILESIZE: int
    LOG_FILES_LIMIT: int

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str


@lru_cache
def get_config() -> dict:
    """Create config object from dotenv file."""
    config_values = dotenv_values(DOTENV_FILE)
    config = Dotenv()

    for key in config_values:
        value = config_values[key]

        if Dotenv.__annotations__[key] == str:
            setattr(config, key, value)

        elif Dotenv.__annotations__[key] == int:
            setattr(config, key, int(value))

        elif Dotenv.__annotations__[key] == bool:
            setattr(config, key, True if value.lower() == "true" else False)

        else:
            setattr(config, key, None)

    return config
