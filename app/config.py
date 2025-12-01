"""
Configuration management for Astro Engine
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Astro Engine"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = False
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Swiss Ephemeris
    EPHEMERIS_PATH: str = "./ephemeris_data"
    
    # Security
    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Timezone
    DEFAULT_TIMEZONE: str = "Asia/Kolkata"
    
    # Ayanamsa
    AYANAMSA: str = "LAHIRI"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/astro_engine.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Ensure required directories exist
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
os.makedirs(settings.EPHEMERIS_PATH, exist_ok=True)
