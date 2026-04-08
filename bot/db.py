import asyncpg
from bot.config import settings

pool: asyncpg.Pool | None = None


async def create_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(dsn=settings.database_url, min_size=1, max_size=10)
    return pool


async def get_pool() -> asyncpg.Pool:
    if pool is None:
        return await create_pool()
    return pool