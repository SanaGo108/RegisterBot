from pydantic_settings import BaseSettings
from typing import List
from datetime import datetime

class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str
    ADMIN_IDS: List[int]
    EVENT_DATE: datetime

    class Config:
        env_file = ".env"

settings = Settings()
