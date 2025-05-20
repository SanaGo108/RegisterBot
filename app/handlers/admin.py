from aiogram import types, F, Router
from app.config import settings
from app.database.db import get_participant_count, get_all_participants, mark_reminder_sent
from app.utils.exporter import export_to_csv
from app.utils.broadcaster import broadcast

admin_router = Router()

@admin_router.message(F.text == "/list")
async def list_users(message: types.Message):
    if message.from_user.id not in settings.ADMIN_IDS:
        return
    count = await get_participant_count()
    await message.answer(f"Количество участников: {count}")

@admin_router.message(F.text == "/export")
async def export_data(message: types.Message):
    if message.from_user.id not in settings.ADMIN_IDS:
        return
    path = await export_to_csv()
    await message.answer_document(types.FSInputFile(path))

@admin_router.message(F.text.startswith("/broadcast"))
async def broadcast_msg(message: types.Message):
    if message.from_user.id not in settings.ADMIN_IDS:
        return
    text = message.text.split(" ", 1)[1] if " " in message.text else None
    if not text:
        await message.answer("Укажите текст: /broadcast Привет!")
        return
    await broadcast(text)


