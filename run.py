import asyncio
from aiogram import Dispatcher
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.bot import bot
from app.config import settings
from app.scheduler.reminder import send_reminders
from app.database.db import init_db
from app.handlers import router as routers


async def setup_bot_commands():
    commands = [
        BotCommand(command="start", description="Регистрация на мероприятие"),
        BotCommand(command="command1", description="Повтор команды /start"),
    ]
    await bot.set_my_commands(commands)


async def main():
    dp = Dispatcher()

    # Подключаем роутеры
    for r in routers:
        dp.include_router(r)

    # Инициализация БД
    await init_db()

    # Установка команд
    await setup_bot_commands()

    # Запуск планировщика
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_reminders, "interval", minutes=2, args=[bot])
    scheduler.start()

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())




