"""
Application Configuration
"""
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator, Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Project Information
    PROJECT_NAME: str = "Londa APIs"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "FastAPI backend for Londa Rides CC"
    API_V1_STR: str = "/api/v1"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # CORS Configuration
    # Use Union to allow both string (comma-separated) and list
    # This prevents pydantic-settings from trying to parse as JSON
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="CORS allowed origins (comma-separated string or list)"
    )
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            # Handle comma-separated string
            if not v.startswith("[") and not v.startswith("{"):
                return [i.strip() for i in v.split(",") if i.strip()]
            # Try to parse as JSON if it looks like JSON
            try:
                import json
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, ValueError):
                pass
            # Fallback: split by comma
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return v
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="after")
    @classmethod
    def ensure_list(cls, v):
        """Ensure the final value is always a list"""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DRIVER_TOKEN_EXPIRE_DAYS: int = 7
    USER_TOKEN_EXPIRE_DAYS: int = 30
    
    # Firebase Configuration
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    FIREBASE_PROJECT_ID: str = "londa-cd054"
    
    # Google Maps API
    GOOGLE_MAPS_API_KEY: str = "AIzaSyBwA-lP2mV3VIyXesj7bzhvR0WC2sGnTPs"
    
    # SMTP Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "londanase@gmail.com"
    SMTP_PASS: str = "moxb snfc xvoy hroz"
    SMTP_FROM: str = "noreply@londarides.com"
    EMAIL_ACTIVATION_SECRET: str = "QQTRjWtG2EUBqj/aQyEUMvtZutQOSGwCVEu5Yr42uyg="
    
    # Nylas API (optional)
    NYLAS_API_KEY: Optional[str] = "nyk_v0_QcDKjTkTKFJ48xYkPYGOFdKa3phMIrGQ2fhw9p0RPW9C1iCOHFFUu8QVD7S6n3ID"
    
    # Business Constants
    DRIVER_SUBSCRIPTION_AMOUNT: float = 150.00  # NAD per month
    PARENT_SUBSCRIPTION_AMOUNT: float = 1000.00  # NAD per month
    DEFAULT_RIDE_FARE: float = 13.00  # NAD per ride
    
    # FCM Configuration
    # Note: FCM now uses service account credentials (OAuth2) via Firebase Admin SDK
    # No separate FCM_SERVER_KEY needed - uses FIREBASE_CREDENTIALS_PATH
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

