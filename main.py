import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import Message
from config import Config
from database import db
from handlers import register_handlers

class Bot:
    def __init__(self):
        self.client = TelegramClient(
            'bot_session',
            Config.API_ID,
            Config.API_HASH,
            connection_retries=5
        )
        
    async def start(self):
        """Start the bot"""
        # Initialize MongoDB
        await db.init_db()
        
        # Start Telegram client
        await self.client.start(bot_token=Config.BOT_TOKEN)
        print("Bot started successfully!")
        
        # Register all handlers
        await register_handlers(self.client, db)
        
        # Keep the bot running
        await self.client.run_until_disconnected()
        
    async def stop(self):
        """Stop the bot and close connections"""
        await db.close()
        await self.client.disconnect()

if __name__ == "__main__":
    bot = Bot()
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    finally:
        asyncio.run(bot.stop())
