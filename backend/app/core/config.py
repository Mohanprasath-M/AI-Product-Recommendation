import os
from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Product Recommendation & Customer Intelligence Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = "development"

    # Security & JWT
    SECRET_KEY: str = "SUPER_SECRET_PRODUCTION_KEY_CHANGE_IN_ENV_XYZ1234567890"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database: Default to MySQL or SQLite fallback
    # MySQL Workbench typical connection: mysql+pymysql://root:password@localhost:3306/ai_recommendation_db
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../ai_recommendation.db')).replace(chr(92), '/')}"
    )
    
    # Redis URL
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]

    # Recommender Default Weights
    WEIGHT_CONTENT: float = 0.35
    WEIGHT_COLLABORATIVE: float = 0.30
    WEIGHT_BEHAVIOR: float = 0.15
    WEIGHT_POPULARITY: float = 0.08
    WEIGHT_RATING: float = 0.05
    WEIGHT_PERSONALIZATION: float = 0.07

    # Data & ML Paths
    DATA_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data"))
    MODELS_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../ml/saved_models"))

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


settings = Settings()

os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.MODELS_DIR, exist_ok=True)
