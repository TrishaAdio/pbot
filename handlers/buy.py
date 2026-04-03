# Update the process_purchase function in buy.py
async def process_purchase(event, plan_key, package_type, price):
    """Process the purchase"""
    plan = PLANS[plan_key]
    user = await event.get_sender()
    
    # Save purchase to MongoDB
    await db.add_purchase(
        user_id=user.id,
        plan=f"{plan['name']} - {package_type}",
        price=price,
        package_type=package_type
    )
    
    # Get total spent
    total_spent = await db.get_total_spent(user.id)
    
    # Show success message
    buttons = [
        [
            event.client.build_inline_keyboard_button(Messages.BTN_HISTORY, b"history"),
            event.client.build_inline_keyboard_button("🏠 MAIN MENU", b"back")
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
    
    # Send access details
    await event.client.send_message(
        user.id,
        f"🔐 **Access Link:**\nYour content is ready!\n[Click here to access](https://your-content-link.com/plan/{plan_key}/{package_type})\n\n"
        f"💳 **Total spent:** ${total_spent}",
        parse_mode='markdown'
    )
    
    logger.info(f"User {user.id} purchased {plan['name']} - {package_type} for ${price}. Total spent: ${total_spent}")
