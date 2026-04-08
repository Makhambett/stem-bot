def format_request_card(request: dict, manager_name: str | None = None) -> str:
    status = request.get("status", "new")
    status_map = {
        "new": "🆕 Новая",
        "in_progress": "🟡 В процессе",
        "success": "✅ Успешно завершена",
        "failed": "❌ Неуспешно завершена",
    }
    text = (
        f"<b>Заявка #{request['id']}</b>\n"
        f"Статус: {status_map.get(status, status)}\n\n"
        f"👤 Клиент: {request['client_name']}\n"
        f"📞 Телефон: {request['client_phone']}\n"
        f"💬 Сообщение: {request.get('client_message') or '—'}\n"
    )
    if manager_name:
        text += f"\n👨‍💼 Менеджер: {manager_name}\n"
    return text


def format_stats(rows: list[dict]) -> str:
    if not rows:
        return "Статистика пока пустая."
    parts = ["<b>Статистика менеджеров</b>\n"]
    for row in rows:
        parts.append(
            f"👤 {row['name']} (@{row['username'] or 'no_username'})\n"
            f"В работе: {row['in_progress']} | Успешно: {row['success_count']} | Неуспешно: {row['failed_count']} | Всего закрыто: {row['closed_total']}\n"
        )
    return "\n".join(parts)