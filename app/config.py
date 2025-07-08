import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SENTIMENT_API_KEY: str = os.getenv("SENTIMENT_API_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    DATABASE_URL: str = "sqlite:///./complaints.db"
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY")
    SPAM_API_KEY: str = os.getenv("SPAM_API_KEY", "")
    IPAPI_URL: str = "http://ip-api.com/json"

    REQUEST_TIMEOUT: int = 10
    SPAM_THRESHOLD: float = 0.7

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()
