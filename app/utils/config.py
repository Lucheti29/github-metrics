from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    SQL_URL: str
    GITHUB_TOKEN: str
    GITHUB_ORGANIZATION: str

    class Config:
        env_file = "development.env"

@lru_cache()
def get_settings():
    return Settings()