from aiogram import types, F, Router
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from datetime import datetime, timedelta, timezone
from app.database.db import add_participant, mark_reminder_sent
from app.config import settings

user_router = Router()

@user_router.message(F.text.in_({"/start", "/command1"}))
async def start(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Отправить номер", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer(
        "Добро пожаловать! Регистрируйтесь на мероприятие «Бег, Кофе, Танцы». "
        "Пожалуйста, отправьте ваш номер телефона и ник в Telegram.",
        reply_markup=kb
    )

@user_router.message(F.contact)
async def contact_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    phone = message.contact.phone_number

    if not username:
        await message.answer("У вас не установлен username. Пожалуйста, введите его вручную.")
        return

    # Добавляем пользователя в базу
    await add_participant(user_id, username, phone)

    # Сообщаем о регистрации
    await message.answer(
        "Спасибо! Вы зарегистрированы на мероприятие «Бег, Кофе, Танцы». "
        "За день до события мы напомним вам о встрече!",
        reply_markup=ReplyKeyboardRemove()
    )

    # Если осталось меньше суток — отправляем напоминание сразу
    now = datetime.now(timezone.utc)
    event_time = settings.EVENT_DATE.replace(tzinfo=timezone.utc)
    if event_time - now < timedelta(days=1):
        try:
            await message.answer("Напоминаем: завтра мероприятие «Бег, Кофе, Танцы»!")
            await mark_reminder_sent(user_id)
        except Exception as e:
            print(f"Ошибка при отправке напоминания: {e}")
