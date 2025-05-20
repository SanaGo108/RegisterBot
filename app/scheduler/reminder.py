from app.database.db import get_participants_for_reminder, mark_reminder_sent
from datetime import datetime, timedelta, timezone
from app.config import settings

async def send_reminders(bot):
    now = datetime.now(timezone.utc)
    target_time = settings.EVENT_DATE.replace(tzinfo=timezone.utc) - timedelta(days=1)

    delta_seconds = abs((now - target_time).total_seconds())
    print(f"[{now}] Проверка условия отправки: delta = {delta_seconds} сек.")

    if delta_seconds <= 600:  # 10 минутное окно
        participants = await get_participants_for_reminder()
        print(f"Найдено участников для напоминания: {len(participants)}")
        for user in participants:
            try:
                await bot.send_message(user["telegram_user_id"], "Напоминаем: завтра мероприятие «Бег, Кофе, Танцы»!")
                await mark_reminder_sent(user["telegram_user_id"])
                print(f"Отправлено пользователю {user['telegram_user_id']}")
            except Exception as e:
                print(f"Не удалось отправить {user['telegram_user_id']}: {e}")
