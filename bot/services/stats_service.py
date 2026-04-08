from bot.db import get_pool


async def get_all_stats():
    pool = await get_pool()
    query = """
    SELECT
        bm.telegram_id,
        bm.name,
        bm.username,
        COUNT(br.*) FILTER (WHERE br.status = 'in_progress') AS in_progress,
        COUNT(br.*) FILTER (WHERE br.status = 'success') AS success_count,
        COUNT(br.*) FILTER (WHERE br.status = 'failed') AS failed_count,
        COUNT(br.*) FILTER (WHERE br.status IN ('success', 'failed')) AS closed_total
    FROM bot_managers bm
    LEFT JOIN bot_requests br
        ON bm.telegram_id = br.manager_telegram_id
    WHERE bm.is_active = true
    GROUP BY bm.telegram_id, bm.name, bm.username
    ORDER BY bm.name ASC;
    """
    async with pool.acquire() as conn:
        rows = await conn.fetch(query)
    return [dict(r) for r in rows]


async def get_manager_stats(manager_id: int):
    pool = await get_pool()
    query = """
    SELECT
        bm.telegram_id,
        bm.name,
        bm.username,
        COUNT(br.*) FILTER (WHERE br.status = 'in_progress') AS in_progress,
        COUNT(br.*) FILTER (WHERE br.status = 'success') AS success_count,
        COUNT(br.*) FILTER (WHERE br.status = 'failed') AS failed_count,
        COUNT(br.*) FILTER (WHERE br.status IN ('success', 'failed')) AS closed_total
    FROM bot_managers bm
    LEFT JOIN bot_requests br
        ON bm.telegram_id = br.manager_telegram_id
    WHERE bm.telegram_id = $1 AND bm.is_active = true
    GROUP BY bm.telegram_id, bm.name, bm.username;
    """
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, manager_id)
    return dict(row) if row else None