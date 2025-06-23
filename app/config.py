from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql://postgres:postgres@localhost:5432/spades3"
    
    # Application settings
    app_name: str = "Spades3 API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # CORS settings
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # WebSocket settings
    websocket_ping_interval: int = 20
    websocket_ping_timeout: int = 20
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings() 