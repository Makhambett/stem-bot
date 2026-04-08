from bot.db import get_pool


async def upsert_manager(telegram_id: int, name: str, username: str | None, role: str = "manager"):
    pool = await get_pool()
    query = """
    INSERT INTO bot_managers (telegram_id, name, username, role, is_busy, total_processed, created_at, is_active)
    VALUES ($1, $2, $3, $4, false, 0, now(), true)
    ON CONFLICT (telegram_id)
    DO UPDATE SET
        name = EXCLUDED.name,
        username = EXCLUDED.username,
        role = EXCLUDED.role,
        is_active = true
    RETURNING telegram_id, name, username, role, is_active;
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, telegram_id, name, username, role)


async def get_manager(telegram_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            "SELECT telegram_id, name, username, role, is_active FROM bot_managers WHERE telegram_id = $1",
            telegram_id,
        )


async def list_managers():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT telegram_id, name, username, role, is_active FROM bot_managers ORDER BY created_at ASC"
        )
    return [dict(r) for r in rows]


async def deactivate_manager(telegram_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.execute(
            "UPDATE bot_managers SET is_active = false WHERE telegram_id = $1", telegram_id
        )