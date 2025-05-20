"""Application settings and configuration."""
import os
import torch
from functools import lru_cache
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings."""
    # Application
    APP_NAME: str = "PCOS Research RAG"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENV: str = os.getenv("ENV", "development")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/pcos_rag")
    
    # Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    
    # FAIRChem
    FAIRCHEM_MODEL: str = os.getenv("FAIRCHEM_MODEL", "facebook/uma")
    FAIRCHEM_DEVICE: str = os.getenv("FAIRCHEM_DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
    
    # 310.ai
    THREETEN_AI_API_KEY: Optional[str] = os.getenv("THREETEN_AI_API_KEY")
    
    # Adaptive Biotechnologies
    ADAPTIVE_BIOTECH_API_KEY: Optional[str] = os.getenv("ADAPTIVE_BIOTECH_API_KEY")
    ADAPTIVE_BIOTECH_API_URL: str = os.getenv("ADAPTIVE_BIOTECH_API_URL", "https://api.adaptivebiotech.com")
    
    # CORS
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Model configuration
    MODEL_CONFIG = {
        "fairchem": {
            "model_name": "uma_sm.pt",
            "task_name": "omol",  # omol for molecules, oc20 for catalysis, etc.
            "device": "cuda" if torch.cuda.is_available() else "cpu"
        },
        "three_ten_ai": {
            "api_key": "",
            "base_url": "https://api.310.ai/v1"
        },
        "adaptive_biotech": {
            "api_key": "",
            "base_url": ADAPTIVE_BIOTECH_API_URL
        }
    }
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings()

# Initialize settings
settings = get_settings()
