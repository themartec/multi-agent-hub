import os
import json
import boto3
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from botocore.exceptions import ClientError


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    JINA_API_KEY: str
    
    LANGSMITH_TRACING: bool
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str
    
    PROXY_USER: str
    PROXY_PWD: str
    
    POSTGRES_URI: str
    REDIS_URI: str
    IMAGE_NAME: str
    
    model_config = SettingsConfigDict(
        env_file=('.prod.env', '.env', '.test.env', '.dev.env'), 
        env_file_encoding='utf-8',
        extra='ignore'
    )


def get_aws_secret(secret_name: str, region_name: str = "us-east-1"):
    """Get secret from AWS Secrets Manager"""
    try:
        client = boto3.client('secretsmanager', region_name=region_name)
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except ClientError as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        return {}


@lru_cache
def get_settings():
    build_env: str = os.getenv("BUILD_ENVIRONMENT", "dev")
    print(f"BUILD_ENVIRONMENT: {build_env}")
    
    # Load base settings from env files
    # if "devCloud" in build_env:
    settings = Settings(_env_file=f'.env', _env_file_encoding='utf-8')
    # else:
    #     settings = Settings(_env_file=f'environment/.{build_env}.env', _env_file_encoding='utf-8')
    
    # Override with AWS secrets in production environments
    # if build_env in ["prod", "staging"]:
    aws_secrets = get_aws_secret(f"/development/langgraph")
    
    # Override settings with AWS values
    for key, value in aws_secrets.items():
        if hasattr(settings, key):
            setattr(settings, key, value)
    
    return settings


settings = get_settings()