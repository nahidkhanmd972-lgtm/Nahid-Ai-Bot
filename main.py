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

# Render Health Check Timed Out সমস্যা সমাধানের জন্য ডামি সার্ভার
def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# Environment Variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Adsterra Direct Link & Admin Email
ADSTERRA_DIRECT_LINK = "https://www.highratecpmgate.com/your_adsterra_link_here"
ADMIN_EMAIL = "nahidkhanmd972@gmail.com"

# Gemini Client ইনিশিয়ালাইজেশন
client = genai.Client(api_key=GEMINI_API_KEY)

# Gemini-কে দেওয়া নির্দেশাবলি
system_prompt = (
    "তোমার নাম NAHID-AI। তোমাকে তৈরি করেছেন Md Nahid Hossen। "
    "তুমি খুব দ্রুত, অত্যন্ত স্মার্ট এবং সুনির্দিষ্টভাবে বাংলা ভাষায় উত্তর দেবে। "
    "কেউ তোমার নাম বা পরিচয় জানতে চাইলে বলবে: "
    "'আমি NAHID-AI, Md Nahid Hossen-এর তৈরি আপনার AI অ্যাসিস্ট্যান্ট। কীভাবে সাহায্য করতে পারি?'"
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# /start কমান্ড হ্যান্ডলার
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

# বাটন ক্লিক হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "opt_photo":
        msg = (
            "📸 **ছবি এডিটিং ও এআই বিশ্লেষণ:**\n\n"
            "আপনার ছবিটি এখানে সেন্ড করুন এবং ছবির সাথে ক্যাপশনে লিখে দিন আপনি কী করতে চান:\n"
            "• ছবি বিশ্লেষণ করা\n"
            "• এডিটিং নির্দেশাবলি বা ব্যাকগ্রাউন্ড আইডিয়া\n"
            "• পাসপোর্ট সাইজ ফটো টিপস\n\n"
            "👉 *একটি ছবি পাঠিয়ে পরীক্ষা করে দেখুন!*"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif query.data == "opt_malaysia":
        msg = (
            "🇲🇾 **মালয়েশিয়া প্রবাসীদের জন্য বিশেষ নোটিশ:**\n\n"
            "আমরা একটি বড় আপডেট আনছি! খুব শীঘ্রই এই বাটনে পাবেন:\n"
            "✅ CIDB কার্ড চেক করার সঠিক পোর্টাল\n"
            "✅ Visa status & Medical test চেক\n"
            "✅ বাংলাদেশ হাই কমিশন মালয়েশিয়া সার্ভিসসমূহ\n"
            "✅ রি-হায়ারিং ও কাজের দরকারি সব অফিশিয়াল ওয়েবসাইট!\n\n"
            "🚀 *কাজ চলছে... খুব দ্রুতই লিংকগুলো যুক্ত হবে। বটটি পিন করে রাখুন!*"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif query.data == "opt_bd_gov":
        msg = (
            "🇧🇩 **পাসপোর্ট ও বাংলাদেশ সরকারি সেবা (Upcoming):**\n\n"
            "সকল সরকারি পোর্টাল এক ক্লিকে পেতে আপডেট আসছে:\n"
            "📌 ই-পাসপোর্ট (E-Passport) আবেদন ও স্ট্যাটাস চেক\n"
            "📌 এনআইডি (NID) সংশোধন ও অনলাইন কপি\n"
            "📌 জন্ম নিবন্ধন অনলাইন যাচাইকরণের ওয়েবসাইট\n\n"
            "⏳ *আপডেট পেতে সাথেই থাকুন।*"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif query.data == "opt_help":
        msg = (
            "💡 **যেকোনো প্রশ্ন / সাহায্য:**\n\n"
            "আপনার যা জানার দরকার চ্যাট বক্সে টাইপ করে পাঠিয় দিন। NAHID-AI সাথে সাথে উত্তর দেবে।"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif query.data == "opt_admin":
        msg = (
            f"👤 **এডমিন এর সাথে যোগাযোগ:**\n\n"
            f"জরুরি সহায়তার জন্য এডমিনকে সরাসরি ইমেইল করুন:\n"
            f"📧 `{ADMIN_EMAIL}`"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

# ছবি প্রসেসিং
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ আপনার ছবি প্রসেস করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")
    
    user_caption = update.message.caption if update.message.caption else "Describe and analyze this image in detail."
    
    try:
        photo_file = await update.message.photo[-1].get_file()
        file_path = "temp_image.jpg"
        await photo_file.download_to_drive(file_path)

        import PIL.Image
        img = PIL.Image.open(file_path)
        
        # Gemini-1.5-flash মডেল ব্যবহার (ছবি দ্রুত প্রসেসের জন্য সেরা)
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
            f"🔓 **এইচডি রেজোলিউশনে দেখতে ও ফাইল ডাউনলোড করতে:**\n"
            f"👉 [এখানে ক্লিক করুন]({ADSTERRA_DIRECT_LINK})"
        )
        await update.message.reply_text(reply_message, parse_mode="Markdown")

    except Exception as e:
        if "429" in str(e):
            await update.message.reply_text("⚠️ অতিরিক্ত রিকোয়েস্ট এসেছে। অনুগ্রহ করে ১৫ সেকেন্ড পর আবার চেষ্টা করুন।")
        else:
            await update.message.reply_text(f"একটি সমস্যা হয়েছে: {str(e)}")

# টেক্সট চ্যাট
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # Gemini-1.5-flash মডেল ব্যবহার (স্মার্ট ও দ্রুত রেসপন্সের জন্য)
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=user_text,
            config={'system_instruction': system_prompt}
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        if "429" in str(e):
            await update.message.reply_text("⚠️ লিমিট পার হওয়ায় সার্ভার ব্যস্ত। ১৫ সেকেন্ড পর আবার চেষ্টা করুন।")
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