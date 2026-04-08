import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    admin_id: int = int(os.getenv("ADMIN_ID", "0"))
    managers_group_id: int = int(os.getenv("MANAGERS_GROUP_ID", "0"))
    database_url: str = os.getenv("DATABASE_URL", "")
    manager_ids: list[int] = None

    def __post_init__(self):
        ids = []
        for key in ("MANAGER_1_ID", "MANAGER_2_ID", "MANAGER_3_ID"):
            value = os.getenv(key)
            if value:
                ids.append(int(value))
        self.manager_ids = ids

settings = Settings()