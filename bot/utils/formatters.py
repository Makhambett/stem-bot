from datetime import datetime
from typing import Optional


def format_request_card(request: dict, manager_name: Optional[str] = None) -> str:
    """Форматирует карточку заявки для отображения в боте"""
    status_emoji = {
        "new": "🆕",
        "in_progress": "🟡",
        "success": "✅",
        "failed": "❌",
    }.get(request["status"], "❓")

    card = f"{status_emoji} <b>Заявка #{request['id']}</b>\n\n"
    card += f"👤 <b>Клиент:</b> {request.get('client_name') or '—'}\n"
    card += f"📞 <b>Телефон:</b> {request.get('client_phone') or request.get('phone') or '—'}\n"
    card += f"💬 <b>Сообщение:</b> {request.get('client_message') or request.get('comment') or '—'}\n"
    
    # Статус и менеджер
    card += f"\n📊 <b>Статус:</b> {request['status']}"
    if manager_name:
        card += f"\n👨‍💼 <b>Менеджер:</b> {manager_name}"
    elif request.get("manager_telegram_id"):
        card += f"\n👨‍ <b>Менеджер:</b> #{request['manager_telegram_id']}"
    
    # Даты с безопасной проверкой типа
    created = request.get("created_at")
    if created and hasattr(created, "strftime"):
        card += f"\n🕐 <b>Создана:</b> {created.strftime('%d.%m.%Y %H:%M')}"
    
    taken = request.get("taken_at")
    if taken and hasattr(taken, "strftime"):
        card += f"\n🕐 <b>Взята:</b> {taken.strftime('%d.%m.%Y %H:%M')}"
    
    closed = request.get("closed_at")
    if closed and hasattr(closed, "strftime"):
        card += f"\n🕐 <b>Закрыта:</b> {closed.strftime('%d.%m.%Y %H:%M')}"
    
    if request.get("result_comment"):
        card += f"\n📝 <b>Комментарий:</b> {request['result_comment']}"
    
    return card


def format_admin_team_card(manager: dict, current_request: dict | None) -> str:
    """Форматирует карточку менеджера для панели админа"""
    status_emoji = "🟢 Свободен" if not manager.get("is_busy") else "🔴 Занят"
    name = manager.get("name") or manager.get("username") or f"ID:{manager['telegram_id']}"
    
    card = f"👤 <b>{name}</b>\n{status_emoji}"
    
    if current_request:
        card += f"\n📌 В работе: #{current_request['id']} ({current_request['client_name']})"
    else:
        card += "\n📌 Нет активных заявок"
    
    if manager.get("total_processed") is not None:
        card += f"\n📊 Всего обработано: {manager['total_processed']}"
    
    return card


def format_manager_personal_card(manager_name: str, current: dict | None, history: list[dict]) -> str:
    """Форматирует личную панель менеджера с текущей заявкой и историей"""
    card = f"📊 <b>Личная панель: {manager_name}</b>\n\n"
    
    # Текущая активная заявка
    if current:
        card += f"🟡 <b>Текущая заявка:</b>\n"
        card += f"ID: #{current['id']}\n"
        card += f"Клиент: {current['client_name']}\n"
        card += f"Телефон: {current.get('phone') or '—'}\n"
        
        created = current.get('created_at')
        if created and hasattr(created, 'strftime'):
            card += f"Создана: {created.strftime('%d.%m %H:%M')}\n\n"
        else:
            card += f"Создана: {created or '—'}\n\n"
    else:
        card += "🟢 <b>Нет активных заявок</b>\n\n"
        
    # История закрытых заявок
    card += "📜 <b>Последние закрытые:</b>\n"
    if not history:
        card += "Пока нет завершённых заявок."
    else:
        for h in history:
            emoji = "✅" if h["status"] == "success" else "❌"
            closed = h.get("closed_at")
            if closed and hasattr(closed, 'strftime'):
                closed_time = closed.strftime("%d.%m %H:%M")
            else:
                closed_time = "—"
            card += f"{emoji} #{h['id']} {h['client_name']} → {closed_time}\n"
            
    return card


def format_stats(stats: dict) -> str:
    card = "📈 <b>Личная статистика</b>\n\n"
    card += f"📦 Всего заявок: {stats.get('total', 0)}\n"
    card += f"🆕 Новые: {stats.get('new', 0)}\n"
    card += f"🟡 В работе: {stats.get('in_progress', 0)}\n"
    card += f"✅ Успешно: {stats.get('success', 0)}\n"
    card += f"❌ Отклонено: {stats.get('failed', 0)}\n"
    
    total = stats.get('total', 0)
    if total > 0:
        success_rate = round(stats.get('success', 0) / total * 100)
        card += f"\n📈 Конверсия: {success_rate}%"
        
    return card