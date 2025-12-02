"""
Pydantic схемы для валидации данных (DTO)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Базовая схема User"""
    telegram_user_id: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    """Схема создания User"""
    pass


class UserUpdate(BaseModel):
    """Схема обновления User"""
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[str] = None


class UserResponse(UserBase):
    """Схема ответа User (для API)"""
    id: int
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    is_active: bool
    is_premium: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserGoalBase(BaseModel):
    """Базовая схема UserGoal"""
    goal_type: str  # 'lose', 'maintain', 'gain'
    target_weight_kg: float
    target_calories: int
    target_protein_g: float
    target_fat_g: float
    target_carbs_g: float


class UserGoalCreate(UserGoalBase):
    """Создание цели"""
    pass


class UserGoalResponse(UserGoalBase):
    """Ответ с целью"""
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserPreferenceBase(BaseModel):
    """Базовая схема UserPreference"""
    dietary_restrictions: Optional[str] = None
    allergies: Optional[str] = None
    disliked_ingredients: Optional[str] = None
    preferred_cuisines: Optional[str] = None
    cooking_methods_allowed: Optional[str] = None


class UserPreferenceCreate(UserPreferenceBase):
    """Создание предпочтений"""
    pass


class UserPreferenceResponse(UserPreferenceBase):
    """Ответ с предпочтениями"""
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
