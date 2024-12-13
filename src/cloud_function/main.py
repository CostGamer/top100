import asyncio
import time

from cloud_function_logic import fetch_parse_push_to_db_repo
from get_db import init_async_pool


async def main() -> None:
    async with await init_async_pool() as pool:
        await fetch_parse_push_to_db_repo(pool)


def handler(event, context) -> None:  # type: ignore
    start_time = time.time()
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        print(f"Execution time: {time.time() - start_time:.2f} seconds")
