"""Config."""

from dotenv import dotenv_values
from functools import lru_cache

DOTENV_FILE = "/hide/.env"

class Config:
    """Config dataclass."""

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str
    POSTGRES_AUTOCOMMIT: bool
    POSTGRES_AUTOFLUSH: bool


@lru_cache
def get_config() -> dict:
    """Create config object from dotenv file."""
    config_values = dotenv_values(DOTENV_FILE)

    for key in config_values:
        if Config.__annotations__[key] == int:
            config_values[key] = int(config_values[key])

        elif Config.__annotations__[key] == bool:
            config_values[key] = True if config_values[key].lower() == "true" else False

        elif Config.__annotations__[key] == None:
            config_values[key] = None

    return config_values
