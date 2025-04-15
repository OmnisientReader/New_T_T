
import os

from pydantic import PostgresDsn, Field, model_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Any, Dict

class Settings(BaseSettings):

    DATABASE_URL: PostgresDsn


    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "restaurant_db"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432


    @model_validator(mode='before')
    @classmethod
    def build_database_url(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Construct DATABASE_URL string from components if it's not provided explicitly.
        Runs before field validation.
        """

        if values.get('DATABASE_URL'):

            pass
        else:

            db_user = values.get('POSTGRES_USER', 'postgres')
            db_password = values.get('POSTGRES_PASSWORD', 'password')
            db_host = values.get('POSTGRES_HOST', 'db')
            db_port = values.get('POSTGRES_PORT', 5432)
            db_name = values.get('POSTGRES_DB', 'restaurant_db')

            constructed_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            values['DATABASE_URL'] = constructed_url


        if 'DATABASE_URL' not in values:
             raise ValueError("DATABASE_URL could not be constructed or found.")

        return values


    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )


try:
    settings = Settings()

except ValidationError as e:
    print(f"Error loading settings: {e}")
    raise
