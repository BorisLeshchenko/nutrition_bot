"""
Конфигурация приложения
"""
from pydantic_settings import BaseSettings
from pathlib import Path

# Путь к корню проекта
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    """Основные настройки приложения"""
    
    # Database
    DATABASE_URL: str
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str
    
    # Server
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    
    class Config:
        env_file = BASE_DIR / ".env"  # Явный путь к .env в корне проекта
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
