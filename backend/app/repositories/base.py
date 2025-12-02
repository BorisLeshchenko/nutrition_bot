"""
Базовый репозиторий с общими CRUD операциями
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Generic, TypeVar, List, Optional
import logging

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """Базовый класс для репозиториев"""
    
    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self.session = session
        self.model = model
    
    async def create(self, obj: ModelType) -> ModelType:
        """Создать объект"""
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        logger.info(f"✅ Создан {self.model.__name__}: {obj.id}")
        return obj
    
    async def get_by_id(self, obj_id: int) -> Optional[ModelType]:
        """Получить объект по ID"""
        result = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Получить все объекты с пагинацией"""
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def update(self, obj_id: int, update_data: dict) -> Optional[ModelType]:
        """Обновить объект"""
        obj = await self.get_by_id(obj_id)
        if not obj:
            return None
        
        for key, value in update_data.items():
            if value is not None and hasattr(obj, key):
                setattr(obj, key, value)
        
        await self.session.commit()
        await self.session.refresh(obj)
        logger.info(f"✅ Обновлён {self.model.__name__}: {obj.id}")
        return obj
    
    async def delete(self, obj_id: int) -> bool:
        """Удалить объект"""
        obj = await self.get_by_id(obj_id)
        if not obj:
            return False
        
        await self.session.delete(obj)
        await self.session.commit()
        logger.info(f"✅ Удалён {self.model.__name__}: {obj_id}")
        return True
