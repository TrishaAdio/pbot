from telethon import TelegramClient, events
from telethon.tl.custom import Button
from texts import Messages
from database import Database
from utils import log_user_action, payment_api
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Plan details with correct prices
PLANS = {
    "plan1": {"name": "PLAN 1", "videos": "5,000", "lite_price": 50, "ultra_price": 85},
    "plan2": {"name": "PLAN 2", "videos": "10,000", "lite_price": 89, "ultra_price": 119},
    "plan3": {"name": "PLAN 3", "videos": "25,000", "lite_price": 150, "ultra_price": 250}
}

# Store active payment sessions
active_payments = {}

async def register_buy_handler(client: TelegramClient, db: Database):
    
    @client.on(events.CallbackQuery(data=b"buy_now"))
    async def buy_now_handler(event):
        buttons = [
            [Button.inline(Messages.BTN_PLAN1, b"plan1"), Button.inline(Messages.BTN_PLAN2, b"plan2")],
            [Button.inline(Messages.BTN_PLAN3, b"plan3")],
            [Button.inline(Messages.BTN_BACK, b"back")]
        ]
        
        await event.answer("Select your plan")
        await event.edit(Messages.BUY_NOW_TXT, buttons=buttons, parse_mode='html')
        log_user_action(event.sender_id, event.sender.username, event.sender.first_name, "Opened buy menu")
    
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
        plan = PLANS[plan_key]
        buttons = [
            [Button.inline(Messages.BTN_ULTRA, f"ultra_{plan_key}".encode()), Button.inline(Messages.BTN_LITE, f"lite_{plan_key}".encode())],
            [Button.inline(Messages.BTN_BACK, b"buy_now")]
        ]
        
        await event.answer(f"Selected {plan['name']}")
        await event.edit(
            Messages.PLAN_SELECTED_PAGE.format(
                plan_name=plan['name'],
                video_count=plan['videos'],
                lite_price=plan['lite_price'],
                ultra_price=plan['ultra_price']
            ),
            buttons=buttons,
            parse_mode='html'
        )
    
    @client.on(events.CallbackQuery(data=b"ultra_plan1"))
    async def ultra_plan1_handler(event):
        await initiate_payment(event, "plan1", "ULTRA", PLANS["plan1"]["ultra_price"])
    
    @client.on(events.CallbackQuery(data=b"ultra_plan2"))
    async def ultra_plan2_handler(event):
        await initiate_payment(event, "plan2", "ULTRA", PLANS["plan2"]["ultra_price"])
    
    @client.on(events.CallbackQuery(data=b"ultra_plan3"))
    async def ultra_plan3_handler(event):
        await initiate_payment(event, "plan3", "ULTRA", PLANS["plan3"]["ultra_price"])
    
    @client.on(events.CallbackQuery(data=b"lite_plan1"))
    async def lite_plan1_handler(event):
        await initiate_payment(event, "plan1", "LITE", PLANS["plan1"]["lite_price"])
    
    @client.on(events.CallbackQuery(data=b"lite_plan2"))
    async def lite_plan2_handler(event):
        await initiate_payment(event, "plan2", "LITE", PLANS["plan2"]["lite_price"])
    
    @client.on(events.CallbackQuery(data=b"lite_plan3"))
    async def lite_plan3_handler(event):
        await initiate_payment(event, "plan3", "LITE", PLANS["plan3"]["lite_price"])
    
    async def initiate_payment(event, plan_key, package_type, amount):
    plan = PLANS[plan_key]
    user = event.sender
    
    # Create invoice via API
    merchant_name = f"{plan['name']} {package_type}"
    merchant_desc = f"{plan['videos']} videos - {package_type} package"
    
    # Show loading message
    await event.edit("⏳ Creating payment invoice... Please wait.", parse_mode='html')
    
    invoice = await payment_api.create_invoice(amount, merchant_name, merchant_desc)
    
    if not invoice['success']:
        await event.edit(f"❌ Payment service error: {invoice.get('error', 'Unknown error')}\n\nPlease try again later.", parse_mode='html')
        return
    
    unique_amount = invoice['unique_amount']
    qr_base64 = invoice.get('full_response', {}).get('qr_base64', '')
    upi_link = invoice.get('full_response', {}).get('upi_link', '')
    
    # Store payment session
    session_id = f"{user.id}_{plan_key}_{package_type}_{unique_amount}"
    active_payments[session_id] = {
        'user_id': user.id,
        'plan_key': plan_key,
        'package_type': package_type,
        'amount': amount,
        'unique_amount': unique_amount,
        'status': 'pending',
        'chat_id': event.chat_id,
        'message_id': event.message_id
    }
    
    # Send QR code as photo
    import base64
    from io import BytesIO
    
    if qr_base64:
        # Decode base64 to image
        qr_image_data = base64.b64decode(qr_base64)
        qr_file = BytesIO(qr_image_data)
        qr_file.name = "qr_code.png"
        
        # Send QR code as photo
        await event.client.send_file(
            event.chat_id,
            qr_file,
            caption=Messages.PAYMENT_QR.format(
                plan_name=plan['name'],
                package_type=package_type,
                amount=unique_amount,
                qr_code=""
            ),
            parse_mode='html'
        )
        
        # Edit the original message with buttons
        buttons = [
            [Button.inline(Messages.BTN_CHECK_STATUS, f"check_{session_id}".encode())],
            [Button.inline(Messages.BTN_CANCEL_PAYMENT, b"buy_now")]
        ]
        
        await event.delete()  # Delete the loading message
        await event.client.send_message(
            event.chat_id,
            Messages.PAYMENT_QR.format(
                plan_name=plan['name'],
                package_type=package_type,
                amount=unique_amount,
                qr_code=""
            ),
            buttons=buttons,
            parse_mode='html'
        )
    else:
        # Fallback to text QR if no image
        qr_text = f"""
┌─────────────────────────────┐
│                             │
│   📱 SCAN TO PAY ₹{unique_amount}   │
│                             │
│   UPI Link: {upi_link}      │
│                             │
└─────────────────────────────┘

💳 **UPI Link:** `{upi_link}`
"""
        buttons = [
            [Button.inline(Messages.BTN_CHECK_STATUS, f"check_{session_id}".encode())],
            [Button.inline(Messages.BTN_CANCEL_PAYMENT, b"buy_now")]
        ]
        
        await event.edit(
            Messages.PAYMENT_QR.format(
                plan_name=plan['name'],
                package_type=package_type,
                amount=unique_amount,
                qr_code=qr_text
            ),
            buttons=buttons,
            parse_mode='html'
        )
    
    log_user_action(user.id, user.username, user.first_name, "Initiating payment", f"{plan['name']} {package_type} - ₹{amount}")
    
    # Auto-check payment in background
    asyncio.create_task(check_payment_loop(event.client, event.chat_id, session_id, unique_amount))
    
    async def check_payment_loop(client, chat_id, session_id, amount, timeout=600):
        """Check payment status every 5 seconds for 10 minutes"""
        for _ in range(timeout // 5):
            await asyncio.sleep(5)
            
            if session_id not in active_payments:
                return
            
            if active_payments[session_id]['status'] == 'completed':
                return
            
            result = await payment_api.check_payment(amount)
            
            if result.get('paid'):
                active_payments[session_id]['status'] = 'completed'
                await complete_purchase(client, chat_id, session_id)
                return
        
        # Timeout
        if session_id in active_payments and active_payments[session_id]['status'] == 'pending':
            active_payments[session_id]['status'] = 'timeout'
            await client.send_message(chat_id, Messages.PAYMENT_TIMEOUT, parse_mode='html')
    
    async def complete_purchase(client, chat_id, session_id):
        """Complete the purchase after successful payment"""
        session = active_payments.get(session_id)
        if not session:
            return
        
        plan = PLANS[session['plan_key']]
        user_id = session['user_id']
        
        # Save to database
        await db.add_purchase(
            user_id=user_id,
            plan=f"{plan['name']} - {session['package_type']}",
            price=session['amount'],
            package_type=session['package_type']
        )
        
        buttons = [
            [Button.inline(Messages.BTN_HISTORY, b"history"), Button.inline("🏠 MAIN MENU", b"back")]
        ]
        
        await client.send_message(
            chat_id,
            Messages.PAYMENT_SUCCESS.format(
                amount=session['amount'],
                plan_name=plan['name'],
                package_type=session['package_type'],
                access_link="https://t.me/your_channel/start"
            ),
            buttons=buttons,
            parse_mode='html'
        )
        
        log_user_action(user_id, None, f"User {user_id}", "Payment successful", f"{plan['name']} {session['package_type']} - ₹{session['amount']}")
        
        # Cleanup
        del active_payments[session_id]
    
    @client.on(events.CallbackQuery(data=lambda x: x and x.startswith(b"check_")))
    async def check_payment_handler(event):
        """Manual check payment button"""
        session_id = event.data.decode().split("_")[1]
        
        if session_id not in active_payments:
            await event.answer("Payment session expired!", alert=True)
            return
        
        session = active_payments[session_id]
        result = await payment_api.check_payment(session['unique_amount'])
        
        if result.get('paid'):
            session['status'] = 'completed'
            await complete_purchase(event.client, event.chat_id, session_id)
            await event.answer("Payment confirmed! ✅", alert=True)
        else:
            await event.answer("Payment not received yet. Please complete payment and try again.", alert=True)
