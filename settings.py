import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    JINA_API_KEY: str
    # LANGSMITH_API_KEY: str
    AUTHEN_TOKEN: str
    USER_PWD: str
    USER_NAME: str
    PROXY_USER: str
    PROXY_PWD: str
    model_config = SettingsConfigDict(env_file=('.env', '.test.env', '.dev.env'), env_file_encoding='utf-8',
                                      extra='ignore')


@lru_cache
def get_settings():
    build_env: str = os.getenv("BUILD_ENVIRONMENT", "dev")
    print(f"BUILD_ENVIRONMENT: {build_env}")
    if "devCloud" in build_env:
        settings = Settings(_env_file=f'.env', _env_file_encoding='utf-8')
    else:
        settings = Settings(_env_file=f'environment/.{build_env}.env', _env_file_encoding='utf-8')
    return settings


settings = get_settings()