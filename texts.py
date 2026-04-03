# All bot texts are stored here for easy management

class Messages:
    # Start message
    START = """<b>ʜᴇʟʟᴏ {mention} 👋</b>

<blockquote>ᴠɪᴀ ᴛʜɪs ʙᴏᴛ ʏᴏᴜ ᴄᴀɴ ʙᴜʏ ʜᴅ ᴘʀᴇᴍɪᴜᴍ ᴄᴏɴᴛᴇɴᴛ ᴠɪᴅᴇᴏs ᴀᴛ ᴄʜᴇᴀᴘ ᴘʀɪᴄᴇ!</blockquote>

<b>📁 ᴘʟᴀɴ 𝟷</b> - <i>𝟻𝟶𝟶𝟶+ ᴠɪᴅᴇᴏs</i>
<b>📁 ᴘʟᴀɴ 𝟸</b> - <i>𝟷𝟶,𝟶𝟶𝟶 ᴠɪᴅᴇᴏs</i>
<b>📁 ᴘʟᴀɴ 𝟹</b> - <i>𝟸𝟻,𝟶𝟶𝟶 ᴠɪᴅᴇᴏs</i>

<blockquote>💎 <b>ɪɴsᴛᴀɴᴛ ᴅᴇʟɪᴠᴇʀʏ</b> | <b>ᴘʀɪᴠᴀᴛᴇ ᴀᴄᴄᴇss</b> | <b>ʜᴅ ǫᴜᴀʟɪᴛʏ</b></blockquote>
<blockquote>⏰ <b>ʟɪғᴇᴛɪᴍᴇ ᴠᴀʟɪᴅɪᴛʏ</b> - ᴏɴᴇ ᴛɪᴍᴇ ᴘᴀʏᴍᴇɴᴛ, ʟɪғᴇᴛɪᴍᴇ ᴀᴄᴄᴇss</blockquote>

👇 <b>ᴄʟɪᴄᴋ ʙᴜʏ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ᴘʟᴀɴ ᴀᴄᴛɪᴠᴇ</b> 👇"""

    # Buy Now page text
    BUY_NOW_TXT = """<b>📦 SELECT YOUR PLAN</b>

Choose the perfect plan for your needs:

<b>📁 PLAN 1</b> - <i>5,000+ Videos</i>
💰 <b>Price:</b> $XX

<b>📁 PLAN 2</b> - <i>10,000 Videos</i>
💰 <b>Price:</b> $XX

<b>📁 PLAN 3</b> - <i>25,000 Videos</i>
💰 <b>Price:</b> $XX

<blockquote>💎 All plans include:
✓ Instant delivery
✓ Private access
✓ HD quality
✓ Lifetime validity</blockquote>

👇 <b>Select your plan below</b> 👇"""

    # Plan selected page text
    PLAN_SELECTED_PAGE = """<b>✅ PLAN {plan_name} SELECTED</b>

<b>📁 Plan:</b> {plan_name}
<b>📊 Videos:</b> {video_count}+ videos
<b>💰 Price:</b> ${price}

<blockquote>🎯 <b>Choose your package type:</b></blockquote>

<b>✨ ULTRA</b> - Full access + Bonus content + Priority support
<b>⚡ LITE</b> - Standard access + Basic support

👇 <b>Click below to proceed</b> 👇"""

    # Ultra package details
    ULTRA_PAGE = """<b>🌟 ULTRA PACKAGE SELECTED</b>

<b>📁 Plan:</b> {plan_name} (ULTRA)
<b>📊 Videos:</b> {video_count}+ videos
<b>💰 Price:</b> ${ultra_price}

<blockquote>✨ <b>ULTRA Benefits:</b>
• Full HD & 4K content
• Bonus videos monthly
• Priority 24/7 support
• Early access to new content
• Download allowed
• Lifetime updates</blockquote>

<blockquote>⏰ <b>Lifetime validity</b> - One time payment</blockquote>

✅ <b>Click CONFIRM to complete your purchase</b>"""

    # Lite package details
    LITE_PAGE = """<b>⚡ LITE PACKAGE SELECTED</b>

<b>📁 Plan:</b> {plan_name} (LITE)
<b>📊 Videos:</b> {video_count}+ videos
<b>💰 Price:</b> ${lite_price}

<blockquote>✨ <b>LITE Benefits:</b>
• HD quality content
• Standard support
• Lifetime access
• Download allowed</blockquote>

<blockquote>⏰ <b>Lifetime validity</b> - One time payment</blockquote>

✅ <b>Click CONFIRM to complete your purchase</b>"""

    # Button texts
    BTN_BUY_NOW = "💰 BUY NOW"
    BTN_DEMO = "🎮 DEMO"
    BTN_HISTORY = "📜 HISTORY"
    BTN_PLAN1 = "📁 PLAN 1"
    BTN_PLAN2 = "📁 PLAN 2"
    BTN_PLAN3 = "📁 PLAN 3"
    BTN_ULTRA = "✨ ULTRA"
    BTN_LITE = "⚡ LITE"
    BTN_CONFIRM = "✅ CONFIRM PURCHASE"
    BTN_BACK = "⬅️ BACK"
    BTN_CANCEL = "❌ CANCEL"

    # Demo page
    DEMO_TEXT = """<b>🎮 DEMO VERSION</b>

<blockquote>Check out sample content quality!</blockquote>

<b>📹 Sample Video:</b>
Here's a preview of what you'll get:

[Sample video link or preview]

<blockquote>💎 <b>Full version includes:</b>
✓ {video_count}+ videos
✓ HD/4K quality
✓ Private access
✓ Lifetime validity</blockquote>

👇 <b>Buy full version for complete access</b> 👇"""

    # History page
    HISTORY_TEXT = """<b>📜 PURCHASE HISTORY</b>

{history_list}

<blockquote>💎 Total Spent: ${total_spent}</blockquote>

<i>Thank you for being our customer! ❤️</i>"""

    NO_HISTORY = """<b>📜 PURCHASE HISTORY</b>

<blockquote>You haven't made any purchases yet!</blockquote>

👇 <b>Click BUY NOW to get started</b> 👇"""

    # Purchase success message
    PURCHASE_SUCCESS = """<b>✅ PURCHASE SUCCESSFUL!</b>

<blockquote>🎉 Congratulations! You've successfully purchased:</blockquote>

<b>📁 Plan:</b> {plan_name}
<b>📦 Package:</b> {package_type}
<b>💰 Amount Paid:</b> ${price}

<blockquote>📥 <b>Access Your Content:</b>
[Link to your content will appear here]

💾 Save this message for future reference!</blockquote>

<i>Thank you for your purchase! ❤️</i>"""

# In texts.py, add this if not already there
DEMO_TEXT = """<b>🎮 DEMO VERSION</b>

<blockquote>Check out sample content quality!</blockquote>

<b>📹 Sample Video:</b>
Here's a preview of what you'll get:

[Sample video link or preview]

<blockquote>💎 <b>Full version includes:</b>
✓ 5000+ videos
✓ HD/4K quality
✓ Private access
✓ Lifetime validity</blockquote>

👇 <b>Buy full version for complete access</b> 👇"""
