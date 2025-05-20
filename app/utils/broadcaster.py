from app.database.db import get_all_participants
from app.bot import bot

async def broadcast(text: str):
    users = await get_all_participants()
    for user in users:
        try:
            await bot.send_message(user["telegram_user_id"], text)
        except Exception:
            pass
