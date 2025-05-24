from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional, Union, Any
import json # For parsing list from string

class Settings(BaseSettings):
    PROJECT_NAME: str = "UTM System MVP"
    PROJECT_VERSION: str = "0.1.0"

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "utm_user"
    POSTGRES_PASSWORD: str = "secure_password"
    POSTGRES_DB: str = "utm_db"
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: Optional[str] = None

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    BACKEND_CORS_ORIGINS: Union[str, List[str]] = '["*"]' # Default to allow all

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
            parsed = json.loads(self.BACKEND_CORS_ORIGINS)
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            pass # Fall through to comma-separated logic
        
        # Handle comma-separated string if not a valid JSON list string
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]


    model_config = SettingsConfigDict(env_file=".env", extra='ignore', case_sensitive=True)

settings = Settings()