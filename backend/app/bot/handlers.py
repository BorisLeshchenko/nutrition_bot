"""
Обработчики событий Telegram бота
"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from backend.app.bot.states import UserRegistration
from backend.app.bot.keyboards import get_main_menu, get_gender_keyboard, get_activity_keyboard, get_goal_keyboard
from backend.app.repositories.users_repo import UsersRepository
from backend.app.db.models import User, UserGoal
from backend.app.db.session import async_session_maker

logger = logging.getLogger(__name__)

# Создаём router для хэндлеров
router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Команда /start: начало регистрации"""
    telegram_id = str(message.from_user.id)
    first_name = message.from_user.first_name
    username = message.from_user.username
    
    logger.info(f"👤 /start от пользователя: {telegram_id} ({first_name})")
    
    # Подключаемся к БД и регистрируем пользователя
    async with async_session_maker() as session:
        users_repo = UsersRepository(session)
        user = await users_repo.get_or_create(
            telegram_user_id=telegram_id,
            username=username,
            first_name=first_name
        )
        logger.info(f"✅ Пользователь зарегистрирован/найден: {user.id}")
    
    # Приветствие
    await message.answer(
        f"👋 Привет, {first_name}!\n\n"
        f"Я — твой AI-ассистент по питанию.\n"
        f"Помогу тебе отслеживать калории, получать рекомендации и достигать своих целей! 🎯\n\n"
        f"Давай начнём с профиля. Сколько тебе лет?",
        reply_markup=None
    )
    
    # Переходим в состояние ввода возраста
    await state.set_state(UserRegistration.waiting_for_age)


@router.message(UserRegistration.waiting_for_age)
async def process_age(message: Message, state: FSMContext):
    """Обработка возраста"""
    try:
        age = int(message.text)
        if age < 13 or age > 120:
            await message.answer("❌ Пожалуйста, введи реальный возраст (13-120)")
            return
    except ValueError:
        await message.answer("❌ Пожалуйста, введи число")
        return
    
    await state.update_data(age=age)
    await message.answer(
        "Спасибо! Теперь выбери пол:",
        reply_markup=get_gender_keyboard()
    )
    await state.set_state(UserRegistration.waiting_for_gender)


@router.message(UserRegistration.waiting_for_gender)
async def process_gender(message: Message, state: FSMContext):
    """Обработка пола"""
    gender_map = {
        "👨 Мужской": "M",
        "👩 Женский": "F",
        "⚠️ Другое": "Other"
    }
    
    gender = gender_map.get(message.text)
    if not gender:
        await message.answer("❌ Пожалуйста, выбери из предложенных вариантов")
        return
    
    await state.update_data(gender=gender)
    await message.answer("📏 Укажи свой рост (в см, например: 180)")
    await state.set_state(UserRegistration.waiting_for_height)


@router.message(UserRegistration.waiting_for_height)
async def process_height(message: Message, state: FSMContext):
    """Обработка роста"""
    try:
        height = float(message.text)
        if height < 100 or height > 250:
            await message.answer("❌ Пожалуйста, укажи реальный рост (100-250 см)")
            return
    except ValueError:
        await message.answer("❌ Пожалуйста, введи число")
        return
    
    await state.update_data(height_cm=height)
    await message.answer("⚖️ Укажи свой вес (в кг, например: 75.5)")
    await state.set_state(UserRegistration.waiting_for_weight)


@router.message(UserRegistration.waiting_for_weight)
async def process_weight(message: Message, state: FSMContext):
    """Обработка веса"""
    try:
        weight = float(message.text)
        if weight < 30 or weight > 200:
            await message.answer("❌ Пожалуйста, укажи реальный вес (30-200 кг)")
            return
    except ValueError:
        await message.answer("❌ Пожалуйста, введи число")
        return
    
    await state.update_data(weight_kg=weight)
    await message.answer(
        "💪 Какой у тебя уровень физической активности?",
        reply_markup=get_activity_keyboard()
    )
    await state.set_state(UserRegistration.waiting_for_activity)


@router.message(UserRegistration.waiting_for_activity)
async def process_activity(message: Message, state: FSMContext):
    """Обработка активности"""
    activity_map = {
        "🛋️ Сидячий": "sedentary",
        "🚶 Лёгкая активность": "light",
        "🏃 Умеренная активность": "moderate",
        "💪 Высокая активность": "active",
        "🏋️ Очень высокая": "very_active"
    }
    
    activity = activity_map.get(message.text)
    if not activity:
        await message.answer("❌ Пожалуйста, выбери из предложенных вариантов")
        return
    
    await state.update_data(activity_level=activity)
    await message.answer(
        "🎯 Какова твоя основная цель?",
        reply_markup=get_goal_keyboard()
    )
    await state.set_state(UserRegistration.waiting_for_goal)


@router.message(UserRegistration.waiting_for_goal)
async def process_goal(message: Message, state: FSMContext):
    """Обработка цели"""
    goal_map = {
        "📉 Похудеть": "lose",
        "⚖️ Поддерживать вес": "maintain",
        "📈 Набрать вес": "gain"
    }
    
    goal_type = goal_map.get(message.text)
    if not goal_type:
        await message.answer("❌ Пожалуйста, выбери из предложенных вариантов")
        return
    
    await state.update_data(goal_type=goal_type)
    await message.answer("🎲 Укажи целевой вес (в кг)")
    await state.set_state(UserRegistration.waiting_for_target_weight)


@router.message(UserRegistration.waiting_for_target_weight)
async def process_target_weight(message: Message, state: FSMContext):
    """Обработка целевого веса"""
    try:
        target_weight = float(message.text)
        if target_weight < 30 or target_weight > 200:
            await message.answer("❌ Пожалуйста, укажи реальный целевой вес (30-200 кг)")
            return
    except ValueError:
        await message.answer("❌ Пожалуйста, введи число")
        return
    
    await state.update_data(target_weight_kg=target_weight)
    await message.answer("🍽️ Укажи целевое количество калорий в день (например: 2000)")
    await state.set_state(UserRegistration.waiting_for_calories)


@router.message(UserRegistration.waiting_for_calories)
async def process_calories(message: Message, state: FSMContext):
    """Обработка калорий и завершение регистрации"""
    try:
        calories = int(message.text)
        if calories < 1000 or calories > 5000:
            await message.answer("❌ Пожалуйста, укажи реальное количество калорий (1000-5000)")
            return
    except ValueError:
        await message.answer("❌ Пожалуйста, введи число")
        return
    
    # Получаем все данные профиля
    data = await state.get_data()
    
    # Сохраняем профиль в БД
    telegram_id = str(message.from_user.id)
    async with async_session_maker() as session:
        users_repo = UsersRepository(session)
        user = await users_repo.get_by_telegram_id(telegram_id)
        
        if user:
            # Обновляем профиль пользователя
            await users_repo.update(user.id, {
                "age": data.get("age"),
                "gender": data.get("gender"),
                "height_cm": data.get("height_cm"),
                "weight_kg": data.get("weight_kg"),
                "activity_level": data.get("activity_level")
            })
            
            # Сохраняем цели
            target_weight = data.get("target_weight_kg", 0)
            current_weight = data.get("weight_kg", 0)
            goal_type = data.get("goal_type", "maintain")
            
            # Простой расчёт КБЖУ (для MVP)
            calories_target = calories
            protein = int(calories_target * 0.3 / 4)  # 30% от калорий / 4 ккал на грамм
            fat = int(calories_target * 0.25 / 9)      # 25% от калорий / 9 ккал на грамм
            carbs = int(calories_target * 0.45 / 4)    # 45% от калорий / 4 ккал на грамм
            
            goal = UserGoal(
                user_id=user.id,
                goal_type=goal_type,
                target_weight_kg=target_weight,
                target_calories=calories_target,
                target_protein_g=protein,
                target_fat_g=fat,
                target_carbs_g=carbs
            )
            session.add(goal)
            await session.commit()
            logger.info(f"✅ Цели сохранены для пользователя {user.id}")
    
    # Завершение регистрации
    await message.answer(
        f"✅ Спасибо! Профиль готов! 🎉\n\n"
        f"📊 Твои целевые показатели:\n"
        f"• Калории: {calories} ккал\n"
        f"• Белки: {protein}г | Жиры: {fat}г | Углеводы: {carbs}г\n\n"
        f"Теперь ты готов начать отслеживать питание!",
        reply_markup=get_main_menu()
    )
    
    await state.clear()


@router.message(F.text == "📷 Добавить приём пищи")
async def add_meal(message: Message):
    """Заглушка: добавление приёма пищи"""
    await message.answer("📷 Пока эта функция в разработке. Приходи позже!")


@router.message(F.text == "📊 История питания")
async def meal_history(message: Message):
    """Заглушка: история питания"""
    await message.answer("📊 Пока эта функция в разработке. Приходи позже!")


@router.message(F.text == "💡 Рекомендации")
async def recommendations(message: Message):
    """Заглушка: рекомендации"""
    await message.answer("💡 Пока эта функция в разработке. Приходи позже!")


@router.message(F.text == "⚙️ Мой профиль")
async def my_profile(message: Message):
    """Заглушка: мой профиль"""
    await message.answer("⚙️ Пока эта функция в разработке. Приходи позже!")


@router.message()
async def echo(message: Message):
    """Эхо-обработчик для прочих сообщений"""
    await message.answer(f"Я получил: {message.text}\n\nПожалуйста, используй кнопки меню или команды.")
