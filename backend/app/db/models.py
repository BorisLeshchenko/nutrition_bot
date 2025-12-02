"""
ORM модели SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
from sqlalchemy.sql import func
from datetime import datetime
from backend.app.db.session import Base


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Профиль пользователя
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)  # 'M', 'F', 'Other'
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    activity_level = Column(String(50), nullable=True)  # 'sedentary', 'light', 'moderate', 'active', 'very_active'
    
    # Статус
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    
    # Временные метки
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, telegram_user_id={self.telegram_user_id}, username={self.username})>"


class UserGoal(Base):
    """Модель целей пользователя"""
    __tablename__ = "user_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # FK к users.id
    
    # Цели по весу
    goal_type = Column(String(50), nullable=False)  # 'lose', 'maintain', 'gain'
    target_weight_kg = Column(Float, nullable=False)
    weekly_goal_kg = Column(Float, nullable=True)  # целевое изменение веса в неделю
    
    # Калорийность
    target_calories = Column(Integer, nullable=False)
    target_protein_g = Column(Float, nullable=False)
    target_fat_g = Column(Float, nullable=False)
    target_carbs_g = Column(Float, nullable=False)
    
    # Временные метки
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<UserGoal(id={self.id}, user_id={self.user_id}, goal_type={self.goal_type})>"


class UserPreference(Base):
    """Модель предпочтений пользователя"""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # FK к users.id
    
    # Ограничения и аллергены (JSON-подобные строки, для MVP)
    dietary_restrictions = Column(Text, nullable=True)  # JSON: ["vegan", "gluten-free"]
    allergies = Column(Text, nullable=True)  # JSON: ["nuts", "dairy"]
    disliked_ingredients = Column(Text, nullable=True)  # JSON: ["mushrooms"]
    
    # Предпочтения по кухне
    preferred_cuisines = Column(Text, nullable=True)  # JSON: ["Italian", "Asian"]
    cooking_methods_allowed = Column(Text, nullable=True)  # JSON: ["boiling", "baking"]
    
    # Временные метки
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<UserPreference(id={self.id}, user_id={self.user_id})>"