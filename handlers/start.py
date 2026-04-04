from telethon import TelegramClient, events
from telethon.tl.custom import Button
from texts import Messages
from database import Database
from config import Config
from utils import log_user_action
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def register_start_handler(client: TelegramClient, db: Database):
    
    @client.on(events.NewMessage(pattern='/start'))
    async def start_handler(event):
        user = await event.get_sender()
        mention = user.first_name
        
        buttons = [
            [Button.inline(Messages.BTN_BUY_NOW, b"buy_now")],
            [Button.inline(Messages.BTN_DEMO, b"demo"), Button.inline(Messages.BTN_HISTORY, b"history")]
        ]
        
        await db.add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        await event.respond(
            Messages.START.format(mention=mention),
            buttons=buttons,
            parse_mode='html'
        )
        
        # Log to console with colors
        log_user_action(user.id, user.username, user.first_name, "Started the bot")
        
        # Send log to log channel
        try:
            log_message = f"""
# 📊 **BOT STARTED**

**👤 User:** {user.first_name}
**🆔 ID:** `{user.id}`
**🔖 Username:** @{user.username if user.username else 'N/A'}
**🌐 Status:** New session started
**⏰ Time:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            await client.send_message(Config.LOG_CHANNEL_ID, log_message, parse_mode='markdown')
        except Exception as e:
            logger.error(f"Failed to send log to channel: {e}")
        
        logger.info(f"User {user.id} started the bot")
