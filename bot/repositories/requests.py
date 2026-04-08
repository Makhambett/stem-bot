from bot.db import get_pool


async def create_request(client_name: str, client_phone: str, client_message: str):
    pool = await get_pool()
    query = """
    INSERT INTO bot_requests (client_name, client_phone, client_message, status, manager_telegram_id, created_at, updated_at)
    VALUES ($1, $2, $3, 'new', NULL, now(), now())
    RETURNING id, client_name, client_phone, client_message, status, manager_telegram_id, created_at, updated_at, taken_at, closed_at, result_comment;
    """
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, client_name, client_phone, client_message)
        return dict(row)


async def get_request(request_id: int):
    pool = await get_pool()
    query = """
    SELECT id, client_name, client_phone, client_message, status, manager_telegram_id,
           created_at, updated_at, taken_at, closed_at, result_comment
    FROM bot_requests
    WHERE id = $1
    """
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, request_id)
        return dict(row) if row else None


async def take_request_atomic(request_id: int, manager_id: int):
    pool = await get_pool()
    query = """
    UPDATE bot_requests
    SET status = 'in_progress',
        manager_telegram_id = $1,
        taken_at = now(),
        updated_at = now()
    WHERE id = $2 AND status = 'new'
    RETURNING id, client_name, client_phone, client_message, status, manager_telegram_id,
              created_at, updated_at, taken_at, closed_at, result_comment;
    """
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, manager_id, request_id)
        return dict(row) if row else None


async def close_request_atomic(request_id: int, manager_id: int, final_status: str, result_comment: str | None = None):
    pool = await get_pool()
    query = """
    UPDATE bot_requests
    SET status = $3,
        updated_at = now(),
        closed_at = now(),
        result_comment = COALESCE($4, result_comment)
    WHERE id = $1
      AND manager_telegram_id = $2
      AND status = 'in_progress'
    RETURNING id, client_name, client_phone, client_message, status, manager_telegram_id,
              created_at, updated_at, taken_at, closed_at, result_comment;
    """
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, request_id, manager_id, final_status, result_comment)
        return dict(row) if row else None


async def get_requests_by_manager(manager_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT * FROM bot_requests WHERE manager_telegram_id = $1 ORDER BY created_at DESC",
            manager_id,
        )
    return [dict(r) for r in rows]