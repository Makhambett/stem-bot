from bot.db import get_pool


async def create_request(client_name: str, client_phone: str, client_message: str):
    pool = await get_pool()
    query = """
    INSERT INTO applications (name, phone, comment, status, created_at, updated_at)
    VALUES ($1, $2, $3, 'new', NOW(), NOW())
    RETURNING id, name as client_name, phone as client_phone, comment as client_message, status,
              manager_telegram_id, created_at, updated_at, taken_at, closed_at, result_comment;
    """
    print(f"📝 Создание заявки: name={client_name}, phone={client_phone}")
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, client_name, client_phone, client_message)
        result = dict(row)
        print(f"✅ Заявка создана с ID: {result.get('id')}")
        return result


async def get_request(request_id: int):
    pool = await get_pool()
    query = """
    SELECT id, name as client_name, phone as client_phone, comment as client_message, status,
           manager_telegram_id, created_at, updated_at, taken_at, closed_at, result_comment
    FROM applications
    WHERE id = $1
    """
    print(f"🔍 [get_request] Ищу заявку с ID: {request_id}")
    print(f"🔍 [get_request] Тип request_id: {type(request_id)}")
    
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, request_id)
        if row:
            result = dict(row)
            print(f"✅ [get_request] Найдено: ID={result.get('id')}, status={result.get('status')}")
            return result
        else:
            print(f"❌ [get_request] Заявка с ID={request_id} НЕ найдена в БД")
            try:
                all_rows = await conn.fetch("SELECT id, status FROM applications ORDER BY id DESC LIMIT 5")
                print(f"📋 [get_request] Последние 5 заявок в БД: {[(dict(r)['id'], dict(r)['status']) for r in all_rows]}")
            except Exception as e:
                print(f"⚠️ [get_request] Не удалось получить список заявок: {e}")
            return None


async def take_request_atomic(request_id: int, manager_id: int):
    pool = await get_pool()
    query = """
    UPDATE applications
    SET status = 'in_progress',
        manager_telegram_id = $1,
        taken_at = NOW(),
        updated_at = NOW()
    WHERE id = $2 AND status = 'new'
    RETURNING id, name as client_name, phone as client_phone, comment as client_message, status,
              manager_telegram_id, created_at, updated_at, taken_at, closed_at, result_comment;
    """
    print(f"🔄 [take_request_atomic] Пытаюсь взять заявку ID={request_id}, manager_id={manager_id}")
    
    async with pool.acquire() as conn:
        check_row = await conn.fetchrow("SELECT id, status FROM applications WHERE id = $1", request_id)
        if check_row:
            print(f"📊 [take_request_atomic] Текущий статус заявки {request_id}: {dict(check_row)['status']}")
        else:
            print(f"⚠️ [take_request_atomic] Заявка {request_id} не существует в БД")
        
        row = await conn.fetchrow(query, manager_id, request_id)
        if row:
            result = dict(row)
            print(f"✅ [take_request_atomic] Заявка ID={result.get('id')} успешно взята в работу")
            return result
        else:
            print(f"❌ [take_request_atomic] Не удалось взять заявку ID={request_id}. Возможно, статус не 'new' или заявка уже взята")
            return None


async def close_request_atomic(request_id: int, manager_id: int, final_status: str, result_comment: str | None = None):
    pool = await get_pool()
    query = """
    UPDATE applications
    SET status = $3,
        updated_at = NOW(),
        closed_at = NOW(),
        result_comment = COALESCE($4, result_comment)
    WHERE id = $1
      AND manager_telegram_id = $2
      AND status = 'in_progress'
    RETURNING id, name as client_name, phone as client_phone, comment as client_message, status,
              manager_telegram_id, created_at, updated_at, taken_at, closed_at, result_comment;
    """
    print(f"🔒 [close_request_atomic] Закрываю заявку ID={request_id}, manager_id={manager_id}, status={final_status}")
    
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, request_id, manager_id, final_status, result_comment)
        if row:
            result = dict(row)
            print(f"✅ [close_request_atomic] Заявка ID={result.get('id')} закрыта со статусом {final_status}")
            return result
        else:
            print(f"❌ [close_request_atomic] Не удалось закрыть заявку ID={request_id}")
            return None


async def get_requests_by_manager(manager_id: int):
    pool = await get_pool()
    print(f"📋 [get_requests_by_manager] Получаю заявки для manager_id={manager_id}")
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, name as client_name, phone as client_phone, comment as client_message, status, manager_telegram_id, created_at FROM applications WHERE manager_telegram_id = $1 ORDER BY created_at DESC",
            manager_id,
        )
    result = [dict(r) for r in rows]
    print(f"✅ [get_requests_by_manager] Найдено заявок: {len(result)}")
    return result