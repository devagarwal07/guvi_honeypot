"""
Configuration and environment variables
Centralized settings for the application
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Security
    API_KEY: str = os.getenv("API_KEY", "your-secure-api-key-here")
    
    # Gemini/LLM Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    LLM_MODEL: str = "gemini-pro"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 150
    
    # Callback endpoint
    GUVI_CALLBACK_URL: str = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    
    # Agent behavior settings
    MIN_MESSAGES_BEFORE_END: int = 10  # Increased from 8
    MAX_MESSAGES_PER_SESSION: int = 30  # Increased from 25
    MIN_INTELLIGENCE_ITEMS: int = 3  # Increased from 2
    
    # Scam detection thresholds
    SCAM_KEYWORD_THRESHOLD: int = 2
    CONTEXT_ESCALATION_THRESHOLD: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
