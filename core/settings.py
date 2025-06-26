import os
from dotenv import load_dotenv, find_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    """Class to manage all the environment variables from the .env file"""

    debug: bool = False
    database_url: SecretStr
    rabbitmq_url: SecretStr
    rabbitmq_queue: str
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()