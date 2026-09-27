import logging
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from google import genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# Render Health Check Timed Out সমাধান
def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# Environment Variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

ADSTERRA_DIRECT_LINK = "https://www.highratecpmgate.com/your_adsterra_link_here"
ADMIN_EMAIL = "nahidkhanmd972@gmail.com"

# Gemini Client ইনিশিয়ালাইজেশন
client = genai.Client(api_key=GEMINI_API_KEY)

system_prompt = (
    "তোমার নাম NAHID-AI। তোমাকে তৈরি করেছেন Md Nahid Hossen। "
    "তুমি খুব দ্রুত, স্মার্ট এবং অত্যন্ত বিনয়ীভাবে বাংলা ভাষায় উত্তর দেবে। "
    "কেউ তোমার নাম জানতে চাইলে বা পরিচয় জিজ্ঞেস করলে বলবে: "
    "'আমি NAHID-AI, Md Nahid Hossen-এর তৈরি আপনার AI অ্যাসিস্ট্যান্ট। কীভাবে সাহায্য করতে পারি?'"
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🤖 **NAHID-AI স্মার্ট অ্যাসিস্ট্যান্ট-এ আপনাকে স্বাগতম!**\n\n"
        "আমি **Md Nahid Hossen**-এর তৈরি একটি অল-ইন-ওয়ান AI সার্ভিস বট।\n"
        "আপনার প্রয়োজনীয় সেবাটি নিচের বাটন থেকে নির্বাচন করুন:"
    )
    
    keyboard = [
        [InlineKeyboardButton("📸 ছবি এডিটিং ও এআই বিশ্লেষণ", callback_data="opt_photo")],
        [InlineKeyboardButton("🇲🇾 মালয়েশিয়া প্রবাসী সার্ভিস (আসছে...)", callback_data="opt_malaysia")],
        [InlineKeyboardButton("🇧🇩 পাসপোর্ট ও সরকারি সেবা (আসছে...)", callback_data="opt_bd_gov")],
        [InlineKeyboardButton("💡 যেকোনো প্রশ্ন / এআই হেল্প", callback_data="opt_help")],
        [InlineKeyboardButton("👤 এডমিন হেল্পলাইন", callback_data="opt_admin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "opt_photo":
        msg = (
            "📸 **ছবি এডিটিং ও এআই বিশ্লেষণ:**\n\n"
            "আপনার ছবিটি এখানে সেন্ড করুন এবং ক্যাপশনে লিখে দিন আপনি কী করতে চান।"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif query.data == "opt_malaysia":
        msg = (
            "🇲🇾 **মালয়েশিয়া প্রবাসীদের জন্য বিশেষ নোটিশ:**\n\n"
            "খুব শীঘ্রই এই বাটনে পাবেন CIDB, Visa status ও সরকারি লিঙ্কসমূহ!"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif query.data == "opt_bd_gov":
        msg = (
            "🇧🇩 **পাসপোর্ট ও সরকারি সেবা (Upcoming):**\n\n"
            "ই-পাসপোর্ট, এনআইডি ও জন্ম নিবন্ধন পোর্টাল শীঘ্রই যুক্ত হবে।"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif query.data == "opt_help":
        msg = "💡 **যেকোনো প্রশ্ন বলুন:** আপনার প্রশ্নটি টাইপ করে পাঠান।"
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif query.data == "opt_admin":
        msg = f"👤 **এডমিন যোগাযোগ:**\n📧 `{ADMIN_EMAIL}`"
        await query.message.reply_text(msg, parse_mode="Markdown")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ আপনার ছবি প্রসেস করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")
    
    user_caption = update.message.caption if update.message.caption else "Describe and analyze this image in detail."
    
    try:
        photo_file = await update.message.photo[-1].get_file()
        file_path = "temp_image.jpg"
        await photo_file.download_to_drive(file_path)

        import PIL.Image
        img = PIL.Image.open(file_path)
        
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=[user_caption, img],
            config={'system_instruction': system_prompt}
        )
        
        if os.path.exists(file_path):
            os.remove(file_path)

        reply_message = (
            f"✨ **NAHID-AI বিশ্লেষণ সম্পন্ন করেছে!**\n\n"
            f"📝 **ফলাফল:**\n{response.text}\n\n"
            f"───────────────────\n"
            f"🔓 **ডাউনলোড লিংক:** [এখানে ক্লিক করুন]({ADSTERRA_DIRECT_LINK})"
        )
        await update.message.reply_text(reply_message, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"একটি সমস্যা হয়েছে: {str(e)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=user_text,
            config={'system_instruction': system_prompt}
        )
        await update.message.reply_text(response.text)
    except Exception as e:
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