import asyncio
from app.database.db import init_db, get_participants_for_reminder

async def test():
    await init_db()
    users = await get_participants_for_reminder()
    print(f"Найдено участников без напоминания: {len(users)}")
    for u in users:
        print(dict(u))

if __name__ == "__main__":
    try:
        asyncio.run(test())
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            pass
        else:
            raise
