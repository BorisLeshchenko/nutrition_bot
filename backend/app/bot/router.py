"""
Маршрутизация хэндлеров бота
"""
from aiogram import Router

from backend.app.bot.handlers import router as handlers_router


def get_bot_router() -> Router:
    """Получить главный router с подключёнными хэндлерами"""
    main_router = Router()
    
    # Подключаем handlers router
    main_router.include_router(handlers_router)
    
    return main_router
