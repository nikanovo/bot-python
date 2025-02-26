from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import types
from create_bot import dp, bot, logger
import sys
import os
import logging
from main_router import main_router

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

WEBHOOK_PATH = "/webhook"
APP_URL = "https://bot-python-f07a.onrender.com"
WEBHOOK_URL = APP_URL + WEBHOOK_PATH

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await bot.set_webhook(url=WEBHOOK_URL,
                              allowed_updates=dp.resolve_used_update_types(),
                              drop_pending_updates=True)
        logger.info(f"Webhook set to {WEBHOOK_URL}")
        yield
    finally:
        await bot.delete_webhook()
        logger.info("Webhook removed")

webhook_app = FastAPI(lifespan=lifespan)
dp.include_router(main_router)

@webhook_app.post("/webhook")
async def bot_webhook(request: Request):
    try:
        update = types.Update.model_validate(await request.json(), context={"bot": bot})
        await dp.feed_update(bot, update)
        return {"ok": True}
    except Exception as e:
        logger.error(f"Ошибка при обработке webhook: {e}", exc_info=True)
        return {"ok": False, "error": str(e)}

@webhook_app.get("/")
async def root():
    return {"status": "working"}
