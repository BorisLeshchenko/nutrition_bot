"""
Репозиторий для работы с пользователями
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from backend.app.repositories.base import BaseRepository
from backend.app.db.models import User
import logging

logger = logging.getLogger(__name__)


class UsersRepository(BaseRepository[User]):
    """Репозиторий пользователей"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
    
    async def get_by_telegram_id(self, telegram_user_id: str) -> Optional[User]:
        """Получить пользователя по Telegram ID"""
        result = await self.session.execute(
            select(User).where(User.telegram_user_id == telegram_user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_or_create(self, telegram_user_id: str, username: Optional[str] = None, 
                           first_name: Optional[str] = None) -> User:
        """Получить пользователя или создать если не существует"""
        user = await self.get_by_telegram_id(telegram_user_id)
        
        if user:
            logger.info(f"✅ Пользователь найден: {user.id}")
            return user
        
        # Создаём нового пользователя
        new_user = User(
            telegram_user_id=telegram_user_id,
            username=username,
            first_name=first_name
        )
        return await self.create(new_user)
    
    async def get_active_users(self, limit: int = 100) -> list[User]:
        """Получить активных пользователей"""
        result = await self.session.execute(
            select(User).where(User.is_active == True).limit(limit)
        )
        return result.scalars().all()
