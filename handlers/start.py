from telethon import TelegramClient, events
from telethon.tl.custom import Button
from texts import Messages
from database import Database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def register_start_handler(client: TelegramClient, db: Database):
    
    @client.on(events.NewMessage(pattern='/start'))
    async def start_handler(event):
        """Handle /start command"""
        user = await event.get_sender()
        mention = f"[{user.first_name}](tg://user?id={user.id})"
        
        # Create buttons using Button.inline
        buttons = [
            [
                Button.inline(Messages.BTN_BUY_NOW, b"buy_now"),
                Button.inline(Messages.BTN_DEMO, b"demo"),
                Button.inline(Messages.BTN_HISTORY, b"history")
            ]
        ]
        
        # Save user to database
        await db.add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        # Send message with buttons
        await event.respond(
            Messages.START.format(mention=mention),
            buttons=buttons,
            parse_mode='markdown',
            link_preview=False
        )
        
        logger.info(f"User {user.id} started the bot")
