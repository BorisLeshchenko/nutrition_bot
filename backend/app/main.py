"""
FastAPI приложение с интеграцией Telegram бота и БД
"""
from fastapi import FastAPI, Request
import logging
import asyncio
from contextlib import asynccontextmanager
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from backend.app.config import settings
from backend.app.db.session import init_db, dispose_db, Base, engine
from backend.app.bot.webhooks import handle_telegram_update
from backend.app.bot.handlers import router  # Импортируем твой router!

# Настройка логирования
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Глобальные переменные для бота
bot = None
dp = None
polling_task = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    global bot, dp, polling_task
    
    # === ЗАПУСК ===
    logger.info("🚀 Инициализация приложения...")
    
    # 1. Инициализация БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ БД инициализирована")
    
    # 2. Инициализация Telegram бота
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    storage = MemoryStorage()  # FSM storage для состояний
    dp = Dispatcher(storage=storage)
    
    # 3. Регистрируем твой router с handlers
    dp.include_router(router)
    logger.info("✅ Handlers (router) регистрирован")
    
    # 4. Запускаем polling в отдельной таске
    polling_task = asyncio.create_task(start_polling())
    logger.info("🤖 Telegram polling запущен (async task)")
    
    yield
    
    # === ОСТАНОВКА ===
    logger.info("🛑 Закрытие приложения...")
    
    # 1. Останавливаем polling
    if polling_task and not polling_task.done():
        polling_task.cancel()
        try:
            await polling_task
        except asyncio.CancelledError:
            logger.info("✅ Polling task отменён")
    
    # 2. Закрываем бота
    if bot:
        await bot.session.close()
        logger.info("✅ Telegram bot session закрыт")
    
    # 3. Закрываем БД
    await dispose_db()
    logger.info("✅ Приложение остановлено")


async def start_polling():
    """Запуск polling цикла для получения обновлений от Telegram"""
    try:
        logger.info("📨 Polling цикл начался")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except asyncio.CancelledError:
        logger.info("⏹️ Polling цикл остановлен")
    except Exception as e:
        logger.error(f"❌ Ошибка в polling цикле: {e}", exc_info=True)


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
    # [Future] Для production: используем webhook вместо polling
    return await handle_telegram_update(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG
    )
