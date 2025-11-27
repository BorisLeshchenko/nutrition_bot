# Архитектура MVP чат-бота Nutrition v1.0

## 1. Постановка научной задачи

Разработка модульной сервис-ориентированной архитектуры для персонального AI-помощника по питанию, обеспечивающей высокую производительность при нагрузке 100+ одновременных пользователей, низкую задержку межсервисного взаимодействия (p95 < 200 мс) и масштабируемость.

## 2. Архитектурный стек технологий

| Компонент                   | Технология              | Обоснование выбора                                            |
|-----------------------------|-------------------------|---------------------------------------------------------------|
| Backend API                 | Python 3.11 + FastAPI   | Асинхронность, типизация (Pydantic), автодокументация OpenAPI |
| ORM                         | SQLAlchemy              | Типобезопасность, миграции Alembic                            |
| Telegram Bot                | aiogram 3.x             | Асинхронная обработка webhook'ов                              |
| Реляционная БД              | PostgreSQL 15           | ACID, JSONB для гибридных данных                              |
| Документная БД              | MongoDB 7.x             | Динамический AI-профиль пользователя                          |
| Кэш/Брокер                  | Redis 7.x + RQ          | Sub-ms latency, простота развертывания                        |
| Межсервисное взаимодействие | gRPC + Protocol Buffers | 30-40% выше производительность vs REST/JSON                   |

## 3. Коммуникационные протоколы
Telegram Bot (REST/JSON) → Backend:8000 (FastAPI webhook)
Backend → CV Module:8001 (gRPC/Protobuf)
Backend → NLP Module:8002 (gRPC/Protobuf)
Backend → PostgreSQL:5432 (SQLAlchemy)
Backend → MongoDB:27017 (PyMongo)
Backend → Redis:6379 (aioredis/RQ)

## 4. Структура данных

### PostgreSQL (реляционные сущности)
users (telegram_user_id → PK)
user_goals, user_preferences (FK → users)
meal_sessions, meals, meal_edits (FK → users)
subscriptions, payments (FK → users)

### MongoDB (AI-профиль)
user_dynamic_profiles {
behavioral_patterns: { breakfast_consistency: Number },
emotional_patterns: { message_tone_history: Array },
taste_preferences: { evolution: Array }
}

## 5. Пользовательские сценарии (приоритет реализации)

1. **Сценарий 1**: Регистрация → профиль → цели питания
2. **Сценарий 2**: Фото блюда → CV → Nutritionix → черновик
3. **Сценарий 3**: Редактирование (вес, % съеденного)
4. **Сценарий 4**: Завершение сессии → AI-анализ

## 6. Нагрузочное тестирование

**Гипотеза H1**: p95 latency < 200 мс при 100 concurrent users
**Инструменты**: Locust, Prometheus metrics
**Метрики**: throughput, latency (p50/p95), error rate

## 7. Текущий статус разработки (28.11.2025)

- ✅ Backend: FastAPI + webhook
- ⏳ PostgreSQL + ORM модели
- ⏳ gRPC клиенты (CV, NLP)
- ⏳ Пользовательские сценарии 1-2

---
*Разработчик: [имя], магистратура "Науки о данных", 2025*