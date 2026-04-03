from telethon import TelegramClient, events
from telethon.tl.types import InlineKeyboardButton
from texts import Messages
from database import Database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def register_demo_handler(client: TelegramClient, db: Database):
    
    @client.on(events.CallbackQuery(data=b"demo"))
    async def demo_handler(event):
        """Handle Demo button click"""
        user = await event.get_sender()
        
        buttons = [
            [
                InlineKeyboardButton(text=Messages.BTN_BUY_NOW, callback_data=b"buy_now"),
                InlineKeyboardButton(text=Messages.BTN_BACK, callback_data=b"back")
            ]
        ]
        
        await event.answer("Showing demo...")
        await event.edit(
            Messages.DEMO_TEXT.format(video_count="5,000+"),
            buttons=buttons,
            parse_mode='html'
        )
        
        logger.info(f"User {user.id} viewed demo")
