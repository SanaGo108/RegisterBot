import csv
from app.database.db import get_all_participants

async def export_to_csv():
    participants = await get_all_participants()
    filename = "participants.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Telegram ID", "Username", "Phone", "Registered", "Reminder Sent"])
        for row in participants:
            writer.writerow([
                row["id"],
                row["telegram_user_id"],
                row["username"],
                row["phone_number"],
                row["registration_time"],
                row["reminder_sent"]
            ])
    return filename
