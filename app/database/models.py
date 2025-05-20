from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import (
    Table,
    Column,
    Integer,
    BigInteger,
    String,
    TIMESTAMP,
    Boolean,
    MetaData,
)

# SQLAlchemy metadata для описания таблиц
metadata = MetaData()

# Pydantic-like dataclass (необязательный, но полезный для типизации)
@dataclass
class Participant:
    id: int
    telegram_user_id: int
    username: str
    phone_number: str
    registration_time: datetime
    reminder_sent: bool

# SQLAlchemy-таблица
participants_table = Table(
    "participants",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("telegram_user_id", BigInteger, nullable=False),
    Column("username", String(255)),
    Column("phone_number", String(20)),
    Column("registration_time", TIMESTAMP, default=datetime.utcnow),
    Column("reminder_sent", Boolean, default=False),
)
