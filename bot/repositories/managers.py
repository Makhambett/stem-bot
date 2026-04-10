from bot.db import get_pool


# ==========================================
# 📦 Базовые операции с менеджерами (CRUD)
# ==========================================

async def upsert_manager(telegram_id: int, name: str, username: str | None, role: str = "manager"):
    """Создаёт или обновляет менеджера в БД"""
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
    """Получает данные менеджера по Telegram ID"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT telegram_id, name, username, role, is_active, is_busy FROM bot_managers WHERE telegram_id = $1",
            telegram_id,
        )
        return dict(row) if row else None


async def list_managers():
    """Возвращает список всех активных менеджеров"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT telegram_id, name, username, role, is_active, is_busy FROM bot_managers ORDER BY created_at ASC"
        )
    return [dict(r) for r in rows]


async def deactivate_manager(telegram_id: int):
    """Деактивирует менеджера (не удаляет)"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.execute(
            "UPDATE bot_managers SET is_active = false WHERE telegram_id = $1", telegram_id
        )


# ==========================================
# 🟢 Статус занятости и история заявок
# ==========================================

async def set_manager_busy(telegram_id: int, is_busy: bool):
    """Устанавливает статус занятости менеджера"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE bot_managers SET is_busy = $1 WHERE telegram_id = $2",
            is_busy, telegram_id
        )


async def get_all_managers_status():
    """Получает статус всех менеджеров для админа"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT telegram_id, name, username, is_busy, total_processed "
            "FROM bot_managers WHERE is_active = true ORDER BY telegram_id"
        )
        return [dict(r) for r in rows]


async def get_manager_current_request(telegram_id: int):
    """Получает текущую активную заявку менеджера"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        # 🔧 name AS client_name — алиас для совместимости с formatters.py
        row = await conn.fetchrow(
            "SELECT id, name AS client_name, phone, created_at "
            "FROM applications "
            "WHERE manager_telegram_id = $1 AND status = 'in_progress' "
            "ORDER BY created_at DESC LIMIT 1",
            telegram_id
        )
        return dict(row) if row else None


async def get_manager_history(telegram_id: int, limit: int = 5):
    """Получает историю закрытых заявок менеджера"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        # 🔧 Убрали COALESCE — берём только closed_at
        # NULLS LAST — заявки без даты закрытия уйдут в конец списка
        rows = await conn.fetch(
            "SELECT id, name AS client_name, status, created_at, closed_at "
            "FROM applications "
            "WHERE manager_telegram_id = $1 AND status IN ('success', 'failed') "
            "ORDER BY closed_at DESC NULLS LAST LIMIT $2",
            telegram_id, limit
        )
        return [dict(r) for r in rows]
async def get_manager_stats(telegram_id: int) -> dict:
    """Считает статистику менеджера по заявкам"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT status, COUNT(*) as count FROM applications "
            "WHERE manager_telegram_id = $1 GROUP BY status",
            telegram_id
        )
        
        stats = {"total": 0, "new": 0, "in_progress": 0, "success": 0, "failed": 0}
        for r in rows:
            status = r["status"]
            count = r["count"]
            if status in stats:
                stats[status] = count
                stats["total"] += count
        return stats



async def get_manager_stats(telegram_id: int) -> dict:
    """Считает личную статистику менеджера"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT status, COUNT(*) as count FROM applications "
            "WHERE manager_telegram_id = $1 GROUP BY status",
            telegram_id
        )
        stats = {"total": 0, "new": 0, "in_progress": 0, "success": 0, "failed": 0}
        for r in rows:
            status = r["status"]
            if status in stats:
                stats[status] = r["count"]
                stats["total"] += r["count"]
        return stats