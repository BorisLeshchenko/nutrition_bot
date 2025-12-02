"""
FSM состояния для диалога с пользователем
"""
from aiogram.fsm.state import State, StatesGroup


class UserRegistration(StatesGroup):
    """Состояния регистрации пользователя"""
    waiting_for_age = State()
    waiting_for_gender = State()
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_activity = State()
    waiting_for_goal = State()
    waiting_for_target_weight = State()
    waiting_for_calories = State()
