from bot.db import get_pool
from datetime import datetime, timedelta


async def get_daily_stats() -> dict:
    """Статистика за сегодня"""
    pool = await get_pool()
    now = datetime.now()
    async with pool.acquire() as conn:
        # Передаём datetime-объект напрямую. asyncpg сам преобразует его.
        rows = await conn.fetch(
            "SELECT status, COUNT(*) as cnt FROM applications WHERE created_at::date = $1::date GROUP BY status",
            now
        )
        stats = {"total": 0, "new": 0, "in_progress": 0, "success": 0, "failed": 0}
        for r in rows:
            stats[r["status"]] = r["cnt"]
            stats["total"] += r["cnt"]
        stats["conversion"] = round(stats["success"] / stats["total"] * 100, 1) if stats["total"] > 0 else 0.0
        return stats


async def get_fail_reasons(days: int = 7) -> list[dict]:
    """Причины отказов за последние N дней"""
    pool = await get_pool()
    # Вычисляем дату "N дней назад" как datetime-объект
    since = datetime.now() - timedelta(days=days)
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT result_comment, COUNT(*) as cnt FROM applications "
            "WHERE status = 'failed' AND created_at::timestamptz >= $1::timestamptz "
            "AND result_comment IS NOT NULL AND result_comment != '' "
            "GROUP BY result_comment ORDER BY cnt DESC",
            since  # ✅ Передаём datetime, а не строку
        )
        return [dict(r) for r in rows]


async def get_top_managers(days: int = 7) -> list[dict]:
    """Топ менеджеров по успешным сделкам"""
    pool = await get_pool()
    since = datetime.now() - timedelta(days=days)
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT m.name, m.username, m.telegram_id,
                   COUNT(CASE WHEN a.status = 'success' THEN 1 END) as success_cnt,
                   COUNT(a.id) as total_cnt
            FROM applications a
            JOIN bot_managers m ON a.manager_telegram_id = m.telegram_id
            WHERE a.manager_telegram_id IS NOT NULL AND a.created_at::timestamptz >= $1::timestamptz
            GROUP BY m.telegram_id, m.name, m.username
            ORDER BY success_cnt DESC
            LIMIT 5
            """, since  # ✅ Передаём datetime, а не строку
        )
        results = []
        for r in rows:
            conv = round(r["success_cnt"] / r["total_cnt"] * 100, 1) if r["total_cnt"] > 0 else 0.0
            results.append({
                "name": r["name"] or r["username"] or str(r["telegram_id"]),
                "success": r["success_cnt"],
                "total": r["total_cnt"],
                "conversion": conv
            })
        return results