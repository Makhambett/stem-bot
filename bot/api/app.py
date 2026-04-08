from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from aiogram import Bot
from bot.config import settings
from bot.db import create_pool
from bot.services.notifier_service import notify_new_request
from bot.services.request_service import create_request


class LeadIn(BaseModel):
    client_name: str
    client_phone: str
    client_message: str | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_pool()
    app.state.bot = Bot(token=settings.bot_token)
    yield
    await app.state.bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"ok": True, "service": "stem-bot-api"}


@app.post("/api/leads")
async def create_lead(data: LeadIn):
    request = await create_request(
        client_name=data.client_name,
        client_phone=data.client_phone,
        client_message=data.client_message or "",
    )
    await notify_new_request(app.state.bot, request)
    return {"ok": True, "request_id": request["id"]}