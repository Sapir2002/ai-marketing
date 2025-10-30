# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MOCK_AI: int = 1
    REVIEW_BAD_THRESHOLD: int = 3
    REVIEW_POLL_SECONDS: int = 300
    ENABLE_REVIEW_MONITOR: int = 1

settings = Settings()

