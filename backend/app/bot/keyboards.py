"""
Клавиатуры и кнопки для Telegram бота
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu() -> ReplyKeyboardMarkup:
    """Главное меню"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📷 Добавить приём пищи")],
            [KeyboardButton(text="📊 История питания")],
            [KeyboardButton(text="💡 Рекомендации")],
            [KeyboardButton(text="⚙️ Мой профиль")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard


def get_gender_keyboard() -> ReplyKeyboardMarkup:
    """Выбор пола"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👨 Мужской")],
            [KeyboardButton(text="👩 Женский")],
            [KeyboardButton(text="⚠️ Другое")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_activity_keyboard() -> ReplyKeyboardMarkup:
    """Выбор уровня активности"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛋️ Сидячий")],
            [KeyboardButton(text="🚶 Лёгкая активность")],
            [KeyboardButton(text="🏃 Умеренная активность")],
            [KeyboardButton(text="💪 Высокая активность")],
            [KeyboardButton(text="🏋️ Очень высокая")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_goal_keyboard() -> ReplyKeyboardMarkup:
    """Выбор цели"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📉 Похудеть")],
            [KeyboardButton(text="⚖️ Поддерживать вес")],
            [KeyboardButton(text="📈 Набрать вес")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard
