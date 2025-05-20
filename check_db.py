import asyncio
import asyncpg
from app.config import settings  # чтобы взять DATABASE_URL из конфигурации

async def check_table():
    conn = await asyncpg.connect(settings.DATABASE_URL)

    # Проверяем, существует ли таблица participants
    table_exists = await conn.fetchval("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = 'participants'
        );
    """)

    if not table_exists:
        print("Таблица 'participants' не найдена в базе данных.")
        await conn.close()
        return

    print("Таблица 'participants' найдена. Структура:")

    # Получаем описание колонок (имя и тип данных)
    columns = await conn.fetch("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = 'participants'
        ORDER BY ordinal_position;
    """)

    for col in columns:
        print(f"- {col['column_name']} ({col['data_type']}) "
              f"{'NULLABLE' if col['is_nullable'] == 'YES' else 'NOT NULL'} "
              f"default: {col['column_default']}")

    await conn.close()

if __name__ == "__main__":
    asyncio.run(check_table())
