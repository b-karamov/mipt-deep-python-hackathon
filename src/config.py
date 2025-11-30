import os
from typing import Optional

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./commenthub.db")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
