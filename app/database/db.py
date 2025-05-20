import asyncpg
from app.config import settings
from typing import List, Optional
from datetime import datetime

conn: Optional[asyncpg.Connection] = None
DATABASE_URL = settings.DATABASE_URL


async def init_db():
    """Инициализация соединения и создание таблицы при необходимости."""
    global conn
    if conn is None:
        conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id SERIAL PRIMARY KEY,
            telegram_user_id BIGINT NOT NULL UNIQUE,
            username VARCHAR(255),
            phone_number VARCHAR(20),
            registration_time TIMESTAMP DEFAULT NOW(),
            reminder_sent BOOLEAN DEFAULT FALSE
        )
    ''')


async def add_participant(user_id: int, username: str, phone: str):
    """Добавление участника в БД."""
    await conn.execute('''
        INSERT INTO participants (telegram_user_id, username, phone_number)
        VALUES ($1, $2, $3)
        ON CONFLICT (telegram_user_id) DO NOTHING
    ''', user_id, username, phone)


async def get_participant_count() -> int:
    """Получение количества зарегистрированных участников."""
    return await conn.fetchval('SELECT COUNT(*) FROM participants')


async def get_all_participants() -> List[asyncpg.Record]:
    """Получение всех участников."""
    return await conn.fetch('SELECT * FROM participants')


async def get_participants_for_reminder() -> List[asyncpg.Record]:
    """Получение участников, которым еще не отправлялось напоминание."""
    return await conn.fetch('''
        SELECT * FROM participants 
        WHERE reminder_sent = FALSE OR reminder_sent IS NULL
    ''')


async def mark_reminder_sent(user_id: int):
    """Отметить, что напоминание отправлено."""
    await conn.execute('''
        UPDATE participants 
        SET reminder_sent = TRUE 
        WHERE telegram_user_id = $1
    ''', user_id)
