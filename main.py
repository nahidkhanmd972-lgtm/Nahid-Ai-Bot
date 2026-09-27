import logging
import os
import google.generativeai as genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# Environment Variables থেকে Keys গ্রহণ
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# আপনার Adsterra Direct Link
ADSTERRA_DIRECT_LINK = "https://www.highratecpmgate.com/your_adsterra_link_here"

# এডমিন জিমেইল ঠিকানা
ADMIN_EMAIL = "nahidkhanmd972@gmail.com"

# Gemini API সেটিং
genai.configure(api_key=GEMINI_API_KEY)

system_prompt = (
    "তোমার নাম NAHID-AI। তোমাকে তৈরি করেছেন Md Nahid Hossen। "
    "তুমি খুব দ্রুত, স্মার্ট এবং বিনয়ীভাবে বাংলা ভাষায় উত্তর দেবে। "
    "কেউ তোমার নাম জানতে চাইলে বা পরিচয় জিজ্ঞেস করলে বলবে: "
    "'আমি NAHID-AI, Md Nahid Hossen-এর তৈরি আপনার AI অ্যাসিস্ট্যান্ট। কীভাবে সাহায্য করতে পারি?'"
)

# গুগলের নির্দেশিত লাইভ মডেল
model = genai.GenerativeModel(
    model_name="gemini-3.8-flash",
    system_instruction=system_prompt
)

# লগিং
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# /start কমান্ড (ইনলাইন বাটন সহ অটো মেসেজ)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 **স্বাগতম!**\n\n"
        "আমি **NAHID-AI**, Md Nahid Hossen-এর তৈরি আপনার AI অ্যাসিস্ট্যান্ট।\n\n"
        "আপনার কী ধরনের সেবা প্রয়োজন? নিচের বাটন থেকে বেছে নিন:"
    )
    
    # ইনলাইন ক্লিক্যাবল বাটন
    keyboard = [
        [InlineKeyboardButton("🖼️ ছবি এডিটিং / বিশ্লেষণ", callback_data="opt_photo")],
        [InlineKeyboardButton("💡 যেকোনো প্রশ্ন / সাহায্য", callback_data="opt_help")],
        [InlineKeyboardButton("👤 এডমিনের সাথে যোগাযোগ", callback_data="opt_admin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# বাটন ক্লিকের হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "opt_photo":
        msg = (
            "📸 **ছবি এডিটিং ও বিশ্লেষণ:**\n\n"
            "অনুগ্রহ করে চ্যাট বক্সে আপনার **ছবিটি সেন্ড করুন** এবং সাথে প্রম্পট/নির্দেশনা লিখে দিন (যেমন: 'Background Idea', 'Image analysis')।"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif query.data == "opt_help":
        msg = (
            "💡 **যেকোনো সাহায্য / প্রশ্ন:**\n\n"
            "আপনার প্রশ্নটি চ্যাট বক্সে টাইপ করে পাঠিয়ে দিন। NAHID-AI সাথে সাথে উত্তর তৈরি করে দেবে।"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif query.data == "opt_admin":
        msg = (
            f"👤 **এডমিন এর সাথে যোগাযোগ:**\n\n"
            f"সরাসরি যোগাযোগ বা সহায়তার জন্য ইমেইল করুন:\n"
            f"📧 `{ADMIN_EMAIL}`\n\n"
            f"আপনার বিষয় ইমেইলে লিখে পাঠালে দ্রুত উত্তর পাবেন।"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

# ফটো + প্রম্পট হ্যান্ডলার (Adsterra Monetization)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ আপনার ছবি ও প্রম্পট প্রসেস করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")
    
    user_caption = update.message.caption if update.message.caption else "Describe and analyze this image in detail."
    
    try:
        photo_file = await update.message.photo[-1].get_file()
        file_path = "temp_image.jpg"
        await photo_file.download_to_drive(file_path)

        import PIL.Image
        img = PIL.Image.open(file_path)
        
        response = model.generate_content([user_caption, img])
        
        if os.path.exists(file_path):
            os.remove(file_path)

        reply_message = (
            f"✨ **NAHID-AI বিশ্লেষণ সম্পন্ন করেছে!**\n\n"
            f"📝 **ফলাফল:**\n{response.text}\n\n"
            f"───────────────────\n"
            f"🔓 **এইচডি রেজোলিউশনে দেখতে ও ডাউনলোড করতে লিংক:**\n"
            f"👉 [এখানে ক্লিক করে ফলাফল দেখুন]({ADSTERRA_DIRECT_LINK})"
        )
        await update.message.reply_text(reply_message, parse_mode="Markdown")

    except Exception as e:
        if "429" in str(e):
            await update.message.reply_text("⚠️ লিমিট পার হওয়ায় অনেক রিকোয়েস্ট এসেছে। অনুগ্রহ করে ১৫ সেকেন্ড পর আবার চেষ্টা করুন।")
        else:
            await update.message.reply_text(f"একটি সমস্যা হয়েছে: {str(e)}")

# টেক্সট মেসেজ হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        if "429" in str(e):
            await update.message.reply_text("⚠️ সার্ভারে অতিরিক্ত চাপ থাকায় লিমিট শেষ হয়েছে। অনুগ্রহ করে ১৫ সেকেন্ড পর আবার চেষ্টা করুন।")
        else:
            await update.message.reply_text(f"একটি সমস্যা হয়েছে: {str(e)}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("NAHID-AI Interactive Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

# Background Thread এ ডামি সার্ভার চালু করা
threading.Thread(target=run_dummy_server, daemon=True).start()

# এরপর আপনার বটের আসল কোড থাকবে...