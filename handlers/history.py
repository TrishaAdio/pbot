from telethon import TelegramClient, events
from telethon.types import InlineKeyboardButton
from texts import Messages
from database import Database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def register_history_handler(client: TelegramClient, db: Database):
    
    @client.on(events.CallbackQuery(data=b"history"))
    async def history_handler(event):
        """Handle History button click"""
        user = await event.get_sender()
        
        # Get user's purchase history
        purchases = await db.get_user_purchases(user.id)
        total_spent = await db.get_total_spent(user.id)
        
        if not purchases:
            history_text = Messages.NO_HISTORY
            buttons = [
                [InlineKeyboardButton(text=Messages.BTN_BUY_NOW, callback_data=b"buy_now")],
                [InlineKeyboardButton(text=Messages.BTN_BACK, callback_data=b"back")]
            ]
        else:
            history_list = ""
            for i, purchase in enumerate(purchases, 1):
                history_list += f"\n{i}. **{purchase['plan']}**\n   💰 ${purchase['price']} - {purchase['date']}\n"
            
            history_text = Messages.HISTORY_TEXT.format(
                history_list=history_list,
                total_spent=total_spent
            )
            
            buttons = [
                [InlineKeyboardButton(text=Messages.BTN_BUY_NOW, callback_data=b"buy_now")],
                [InlineKeyboardButton(text=Messages.BTN_BACK, callback_data=b"back")]
            ]
        
        await event.answer("Loading history...")
        await event.edit(
            history_text,
            buttons=buttons,
            parse_mode='markdown'
        )
        
        logger.info(f"User {user.id} viewed history. Total spent: ${total_spent}")
    
    @client.on(events.CallbackQuery(data=b"back"))
    async def back_handler(event):
        """Handle Back button click"""
        user = await event.get_sender()
        mention = f"[{user.first_name}](tg://user?id={user.id})"
        
        # Recreate main menu
        buttons = [
            [
                InlineKeyboardButton(text=Messages.BTN_BUY_NOW, callback_data=b"buy_now"),
                InlineKeyboardButton(text=Messages.BTN_DEMO, callback_data=b"demo"),
                InlineKeyboardButton(text=Messages.BTN_HISTORY, callback_data=b"history")
            ]
        ]
        
        await event.edit(
            Messages.START.format(mention=mention),
            buttons=buttons,
            parse_mode='markdown'
        )
