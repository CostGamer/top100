import asyncio

from src.backend.DB.db import get_db


async def test_db_connection():
    async for conn in get_db():
        print("Подключение установлено")

# Запуск теста
asyncio.run(test_db_connection())
