"""
FastAPI приложение с интеграцией Telegram бота и БД
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import asyncio
from contextlib import asynccontextmanager

from backend.app.config import settings
from backend.app.db.session import init_db, dispose_db, Base, engine
from backend.app.bot.webhooks import handle_telegram_update

# Настройка логирования
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Запуск: инициализация БД
    logger.info("🚀 Инициализация приложения...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ БД инициализирована")
    
    yield
    
    # Остановка: закрытие соединений
    logger.info("🛑 Закрытие приложения...")
    await dispose_db()
    logger.info("✅ Приложение остановлено")


# Создаём приложение с lifespan
app = FastAPI(
    title="Nutrition Bot Backend",
    description="AI-ассистент для трекинга питания",
    version="0.1.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {"message": "Nutrition Bot Backend работает!", "version": "0.1.0"}


@app.get("/healthz")
async def health_check():
    """Проверка здоровья сервиса"""
    logger.info("Health check выполнен")
    return {
        "status": "OK",
        "service": "nutrition-bot-backend",
        "version": "0.1.0"
    }


@app.get("/readyz")
async def ready_check():
    """Проверка готовности сервиса"""
    logger.info("Ready check выполнен")
    return {
        "status": "READY",
        "service": "nutrition-bot-backend"
    }


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    """Приём обновлений от Telegram через webhook"""
    return await handle_telegram_update(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG
    )
