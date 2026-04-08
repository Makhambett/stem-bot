from dataclasses import dataclass
from datetime import datetime


@dataclass
class ManagerSchema:
    telegram_id: int
    name: str
    username: str | None
    role: str
    is_active: bool


@dataclass
class RequestSchema:
    id: int
    client_name: str
    client_phone: str
    client_message: str | None
    status: str
    manager_telegram_id: int | None
    created_at: datetime
    updated_at: datetime
    taken_at: datetime | None = None
    closed_at: datetime | None = None
    result_comment: str | None = None