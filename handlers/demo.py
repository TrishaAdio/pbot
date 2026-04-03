from telethon import TelegramClient, events
from telethon.tl.custom import Button
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
        
        # Create just one back button
        buttons = [
            [Button.inline(Messages.BTN_BACK, b"back")]
        ]
        
        await event.answer("Showing demo...")
        await event.edit(
            Messages.DEMO_TEXT,
            buttons=buttons,
            parse_mode='html'
        )
        
        logger.info(f"User {user.id} viewed demo")
