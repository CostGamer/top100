import asyncio
import time

from src.cloud_function.cloud_function_logic import fetch_parse_push_to_db_repo
from src.cloud_function.get_db import init_async_pool


async def main() -> None:
    async with await init_async_pool() as pool:
        await fetch_parse_push_to_db_repo(pool)


if __name__ == "__main__":
    a = time.time()
    asyncio.run(main())
    print(f"Execution time: {time.time() - a:.2f} seconds")
