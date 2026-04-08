from bot.db import get_pool


async def add_event(request_id: int, actor_telegram_id: int, event_type: str, old_status: str | None, new_status: str | None, comment: str | None = None):
    pool = await get_pool()
    query = """
    INSERT INTO bot_request_events (request_id, actor_telegram_id, event_type, old_status, new_status, comment, created_at)
    VALUES ($1, $2, $3, $4, $5, $6, now())
    RETURNING id;
    """
    async with pool.acquire() as conn:
        return await conn.fetchval(query, request_id, actor_telegram_id, event_type, old_status, new_status, comment)