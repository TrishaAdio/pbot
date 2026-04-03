from telethon import TelegramClient
from database import Database
from .start import register_start_handler
from .buy import register_buy_handler
from .demo import register_demo_handler
from .history import register_history_handler

async def register_handlers(client: TelegramClient, db: Database):
    """Register all handlers"""
    await register_start_handler(client, db)
    await register_buy_handler(client, db)
    await register_demo_handler(client, db)
    await register_history_handler(client, db)
    print("All handlers registered successfully!")
