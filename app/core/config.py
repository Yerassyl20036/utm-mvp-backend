# backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import List, Union
import json

class Settings(BaseSettings):
    PROJECT_NAME: str = "UTM MVP"
    PROJECT_VERSION: str = "0.1.0"

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: Union[str, None] = None # Assembled if not provided

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    BACKEND_CORS_ORIGINS: Union[str, List[str]] # Can be a stringified list or a list

    @property
    def ASSEMBLED_DATABASE_URL(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def PARSED_CORS_ORIGINS(self) -> List[str]:
        if isinstance(self.BACKEND_CORS_ORIGINS, list):
            return self.BACKEND_CORS_ORIGINS
        try:
            # Try to parse if it's a JSON string list
            parsed_origins = json.loads(self.BACKEND_CORS_ORIGINS)
            if isinstance(parsed_origins, list):
                return parsed_origins
        except json.JSONDecodeError:
            # Fallback for comma-separated string
            return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]
        # Default to empty list if parsing fails or it's not a list
        return []


    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()