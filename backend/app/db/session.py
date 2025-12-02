"""
Инициализация SQLAlchemy сессии
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from backend.app.config import settings
import logging

logger = logging.getLogger(__name__)

# Асинхронный движок (asyncpg драйвер)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Логирование SQL если DEBUG=True
    poolclass=NullPool,   # Для локального сервера (MVP)
    future=True
)

# Асинхронная фабрика сессий
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True
)

# Базовый класс для ORM моделей
Base = declarative_base()


async def get_session() -> AsyncSession:
    """Зависимость для FastAPI: получить сессию БД"""
    async with async_session_maker() as session:
        yield session


async def init_db():
    """Инициализация БД: создание всех таблиц"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ БД инициализирована")


async def dispose_db():
    """Закрытие соединений при остановке приложения"""
    await engine.dispose()
    logger.info("✅ Соединения с БД закрыты")