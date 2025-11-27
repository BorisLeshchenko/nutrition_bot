from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Создаём приложение
app = FastAPI(
    title="Nutrition Bot Backend",
    description="AI-ассистент для трекинга питания",
    version="0.1.0"
)

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {"message": "Nutrition Bot Backend работает!"}

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
    """Приём обновлений от Telegram"""
    try:
        update = await request.json()
        logger.info(f"Получен update от Telegram: user_id={update.get('message', {}).get('from', {}).get('id', 'unknown')}")
        logger.debug(f"Полный update: {update}")
        return JSONResponse({"status": "OK"})
    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {str(e)}")
        return JSONResponse({"status": "ERROR"}, status_code=500)

@app.get("/docs")
async def docs_redirect():
    """Перенаправление на документацию"""
    return {"docs": "/docs", "redoc": "/redoc"}
