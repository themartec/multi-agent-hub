import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    JINA_API_KEY: str
    LANGSMITH_API_KEY: str
    AUTHEN_TOKEN: str

    model_config = SettingsConfigDict(env_file=('.prod.env', '.test.env', '.dev.env'), env_file_encoding='utf-8', extra='ignore')


@lru_cache
def get_settings():
    build_env: str = os.getenv("BUILD_ENVIRONMENT", "dev")
    print(f"BUILD_ENVIRONMENT: {build_env}")
    settings = Settings(_env_file=f'environment/.{build_env}.env', _env_file_encoding='utf-8')
    return settings


settings = get_settings()