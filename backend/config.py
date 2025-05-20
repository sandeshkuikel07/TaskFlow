from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "dev"
    
    # Database
    # This will be automatically picked up from environment variables
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS origins can come as a list or comma-separated string from env
    CORS_ORIGINS: Union[str, List[str]] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "allow"  # allow extra env vars without error

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                import json
                return json.loads(v)
            return [origin.strip() for origin in v.split(",")]
        return v

settings = Settings()
