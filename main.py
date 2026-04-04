import asyncio
from telethon import TelegramClient
from config import Config
from database import db
from handlers import register_handlers
from utils import setup_logger, log_user_action
from datetime import datetime

# Setup colored logger
setup_logger()

class Bot:
    def __init__(self):
        self.client = TelegramClient(
            'bot_session',
            Config.API_ID,
            Config.API_HASH,
            connection_retries=5
        )
        
    async def start(self):
        await db.init_db()
        await self.client.start(bot_token=Config.BOT_TOKEN)
        
        # Send bot startup log
        startup_msg = f"""
# 🤖 **BOT STARTED**

**✅ Status:** Online
**⏰ Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**📊 Database:** MongoDB Connected
**💳 Payment API:** {Config.PAYMENT_API_URL}
"""
        try:
            await self.client.send_message(Config.LOG_CHANNEL_ID, startup_msg, parse_mode='markdown')
        except:
            pass
        
        print("\n" + "="*50)
        print("🤖 BOT STARTED SUCCESSFULLY!")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50 + "\n")
        
        await register_handlers(self.client, db)
        await self.client.run_until_disconnected()
        
    async def stop(self):
        await db.close()
        await self.client.disconnect()

if __name__ == "__main__":
    bot = Bot()
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        print("\n⚠️ Bot stopped by user")
    finally:
        asyncio.run(bot.stop())
