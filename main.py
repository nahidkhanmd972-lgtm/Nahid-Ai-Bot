 import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

# আপনার টোকেন এবং ডিপসিক API কী বসান
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
DEEPSEEK_API_KEY = 'YOUR_DEEPSEEK_API_KEY'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# হেল্প ডেস্ক ও মূল মেনু বাটন তৈরির ফাংশন
def get_main_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    
    # বাটনসমূহ
    btn_ai_chat = InlineKeyboardButton("🤖 এআই এর সাথে কথা বলুন", callback_data="btn_ai_chat")
    btn_image_edit = InlineKeyboardButton("🎨 ইমেজ এআই এডিটিং", callback_data="btn_image_edit")
    btn_expat_support = InlineKeyboardButton("🌏 প্রবাসী সাপোর্ট", callback_data="btn_expat_support")
    btn_server_access = InlineKeyboardButton("🖥️ সার্ভার অ্যাক্সেস", callback_data="btn_server_access")
    btn_helpdesk = InlineKeyboardButton("🛠️️ অল হেল্প ডেস্ক", callback_data="btn_helpdesk")
    
    # লেআউট সাজানো
    markup.add(btn_ai_chat)
    markup.add(btn_image_edit, btn_expat_support)
    markup.add(btn_server_access, btn_helpdesk)
    
    return markup

# ডিপসিক API থেকে টেক্সট উত্তর আনার ফাংশন
def get_deepseek_response(user_prompt):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are Nahid AI Assistant. Answer politely and helpfully in Bengali."},
            {"role": "user", "content": user_prompt}
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "দুঃখিত, সিস্টেম কানেকশনে সাময়িক সমস্যা হচ্ছে।"
    except Exception as e:
        return f"ত্রুটি: {str(e)}"

# স্টার্ট কমান্ড (/start) হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 **আসসালামু আলাইকুম!**\n\n"
        "আমি **নাহিদ এআই অ্যাসিস্ট্যান্ট**। আমি আপনাকে কীভাবে সাহায্য করতে পারি?\n\n"
        "✨ **আমাদের সুবিধাসমূহ:**\n"
        "▫️ ২৪/৭ এআই চ্যাট সাপোর্ট\n"
        "▫️ ইমেজ এআই এডিটিং ও ফটো জেনারেশন\n"
        "▫️ প্রবাসীদের জন্য বিশেষ পরামর্শ ও সাপোর্ট\n"
        "▫️ দ্রুত ও স্বয়ংক্রিয় সেবা\n\n"
        "নিচের বাটনগুলো থেকে আপনার প্রয়োজনীয় সার্ভিসটি বেছে নিন:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

# বাটন ক্লিকের রেসপন্স হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    # সার্ভার বা ব্যাকএন্ড ডেভেলপমেন্ট নোটিশ মেসেজ
    under_construction_msg = (
        "⚠️ **সিস্টেম আপডেট নোটিশ!**\n\n"
        "আমাদের এই বটের ডেভেলপমেন্ট ও সার্ভার আপগ্রেডের কাজ দ্রুত গতিতে চলছে।\n\n"
        "⏳ **কাজ সম্পন্ন হতে সর্বমোট ৩ দিন সময় লাগবে।**\n"
        "কাজ শেষ হওয়ার সাথে সাথেই আপনাকে প্রাইভেট মূল অ্যাক্সেস লিংক পাঠিয়ে দেওয়া হবে। আমাদের সাথে থাকার জন্য ধন্যবাদ! ❤️"
    )
    
    if call.data == "btn_ai_chat":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "💬 আপনার প্রশ্নটি লিখে পাঠান, আমি উত্তর দিচ্ছি!")
    else:
        # অন্যান্য সকল বাটন বা হেল্প ডেস্কে ৩ দিনের নোটিশ মেসেজ দেখাবে
        bot.answer_callback_query(call.id, text="কাজ চলছে...", show_alert=False)
        bot.send_message(call.message.chat.id, under_construction_msg, parse_mode="Markdown")

# ছবি হ্যান্ডলার
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_caption = message.caption if message.caption else "ছবিটির সুন্দর একটি বিবরণ দাও।"
    
    processing_msg = bot.reply_to(message, "⏳ নাহিদ এআই চিন্তাভাবনা করছে, একটু অপেক্ষা করুন...")
    
    reply_text = get_deepseek_response(user_caption)
    
    bot.edit_message_text(chat_id=message.chat.id, message_id=processing_msg.message_id, text=reply_text)

# সাধারণ টেক্সট মেসেজ হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    processing_msg = bot.reply_to(message, "⏳ চিন্তা করছি...")
    reply_text = get_deepseek_response(message.text)
    bot.edit_message_text(chat_id=message.chat.id, message_id=processing_msg.message_id, text=reply_text)

print("Nahid AI Bot is Running...")
bot.infinity_polling()
