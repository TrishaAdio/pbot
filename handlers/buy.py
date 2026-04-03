from telethon import TelegramClient, events
from telethon.tl.custom import Button
from texts import Messages
from database import Database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Plan details
PLANS = {
    "plan1": {"name": "PLAN 1", "videos": "5,000", "price": 10, "ultra_price": 15, "lite_price": 10},
    "plan2": {"name": "PLAN 2", "videos": "10,000", "price": 18, "ultra_price": 25, "lite_price": 18},
    "plan3": {"name": "PLAN 3", "videos": "25,000", "price": 35, "ultra_price": 50, "lite_price": 35}
}

async def register_buy_handler(client: TelegramClient, db: Database):
    
    @client.on(events.CallbackQuery(data=b"buy_now"))
    async def buy_now_handler(event):
        """Handle Buy Now button click - Show plan selection"""
        buttons = [
            [
                Button.inline(Messages.BTN_PLAN1, b"plan1"),
                Button.inline(Messages.BTN_PLAN2, b"plan2")
            ],
            [
                Button.inline(Messages.BTN_PLAN3, b"plan3")
            ],
            [
                Button.inline(Messages.BTN_BACK, b"back")
            ]
        ]
        
        await event.answer("Select your plan")
        await event.edit(
            Messages.BUY_NOW_TXT,
            buttons=buttons,
            parse_mode='html'
        )
        
        logger.info(f"User {event.sender_id} opened buy menu")
    
    @client.on(events.CallbackQuery(data=b"plan1"))
    async def plan1_handler(event):
        await show_plan_selection(event, "plan1")
    
    @client.on(events.CallbackQuery(data=b"plan2"))
    async def plan2_handler(event):
        await show_plan_selection(event, "plan2")
    
    @client.on(events.CallbackQuery(data=b"plan3"))
    async def plan3_handler(event):
        await show_plan_selection(event, "plan3")
    
    async def show_plan_selection(event, plan_key):
        """Show Ultra/Lite selection for selected plan"""
        plan = PLANS[plan_key]
        
        buttons = [
            [
                Button.inline(Messages.BTN_ULTRA, f"ultra_{plan_key}".encode()),
                Button.inline(Messages.BTN_LITE, f"lite_{plan_key}".encode())
            ],
            [
                Button.inline(Messages.BTN_BACK, b"buy_now")
            ]
        ]
        
        await event.answer(f"Selected {plan['name']}")
        await event.edit(
            Messages.PLAN_SELECTED_PAGE.format(
                plan_name=plan['name'],
                video_count=plan['videos'],
                price=plan['price']
            ),
            buttons=buttons,
            parse_mode='html'
        )
    
    @client.on(events.CallbackQuery(data=b"ultra_plan1"))
    async def ultra_plan1_handler(event):
        await show_package_details(event, "plan1", "ULTRA")
    
    @client.on(events.CallbackQuery(data=b"ultra_plan2"))
    async def ultra_plan2_handler(event):
        await show_package_details(event, "plan2", "ULTRA")
    
    @client.on(events.CallbackQuery(data=b"ultra_plan3"))
    async def ultra_plan3_handler(event):
        await show_package_details(event, "plan3", "ULTRA")
    
    @client.on(events.CallbackQuery(data=b"lite_plan1"))
    async def lite_plan1_handler(event):
        await show_package_details(event, "plan1", "LITE")
    
    @client.on(events.CallbackQuery(data=b"lite_plan2"))
    async def lite_plan2_handler(event):
        await show_package_details(event, "plan2", "LITE")
    
    @client.on(events.CallbackQuery(data=b"lite_plan3"))
    async def lite_plan3_handler(event):
        await show_package_details(event, "plan3", "LITE")
    
    async def show_package_details(event, plan_key, package_type):
        """Show package details and confirm button"""
        plan = PLANS[plan_key]
        
        if package_type == "ULTRA":
            price = plan['ultra_price']
            text = Messages.ULTRA_PAGE.format(
                plan_name=plan['name'],
                video_count=plan['videos'],
                ultra_price=price
            )
        else:
            price = plan['lite_price']
            text = Messages.LITE_PAGE.format(
                plan_name=plan['name'],
                video_count=plan['videos'],
                lite_price=price
            )
        
        buttons = [
            [
                Button.inline(Messages.BTN_CONFIRM, f"confirm_{plan_key}_{package_type}_{price}".encode())
            ],
            [
                Button.inline(Messages.BTN_BACK, f"{plan_key}".encode())
            ]
        ]
        
        await event.answer(f"Showing {package_type} package details")
        await event.edit(
            text,
            buttons=buttons,
            parse_mode='html'
        )
    
    @client.on(events.CallbackQuery(data=b"confirm_plan1_ULTRA_15"))
    async def confirm_purchase_plan1_ultra(event):
        await process_purchase(event, "plan1", "ULTRA", 15)
    
    @client.on(events.CallbackQuery(data=b"confirm_plan1_LITE_10"))
    async def confirm_purchase_plan1_lite(event):
        await process_purchase(event, "plan1", "LITE", 10)
    
    @client.on(events.CallbackQuery(data=b"confirm_plan2_ULTRA_25"))
    async def confirm_purchase_plan2_ultra(event):
        await process_purchase(event, "plan2", "ULTRA", 25)
    
    @client.on(events.CallbackQuery(data=b"confirm_plan2_LITE_18"))
    async def confirm_purchase_plan2_lite(event):
        await process_purchase(event, "plan2", "LITE", 18)
    
    @client.on(events.CallbackQuery(data=b"confirm_plan3_ULTRA_50"))
    async def confirm_purchase_plan3_ultra(event):
        await process_purchase(event, "plan3", "ULTRA", 50)
    
    @client.on(events.CallbackQuery(data=b"confirm_plan3_LITE_35"))
    async def confirm_purchase_plan3_lite(event):
        await process_purchase(event, "plan3", "LITE", 35)
    
    async def process_purchase(event, plan_key, package_type, price):
        """Process the purchase"""
        plan = PLANS[plan_key]
        user = await event.get_sender()
        
        # Save purchase to database
        await db.add_purchase(
            user_id=user.id,
            plan=f"{plan['name']} - {package_type}",
            price=price,
            package_type=package_type
        )
        
        # Show success message
        buttons = [
            [
                Button.inline(Messages.BTN_HISTORY, b"history"),
                Button.inline("🏠 MAIN MENU", b"back")
            ]
        ]
        
        await event.answer("✅ Purchase successful!", alert=True)
        await event.edit(
            Messages.PURCHASE_SUCCESS.format(
                plan_name=plan['name'],
                package_type=package_type,
                price=price
            ),
            buttons=buttons,
            parse_mode='html'
        )
        
        logger.info(f"User {user.id} purchased {plan['name']} - {package_type} for ${price}")
