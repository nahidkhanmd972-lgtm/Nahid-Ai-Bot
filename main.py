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

# Render Health Check Fix (HTTP Server)
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

# Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

system_prompt = (
    "তোমার নাম NAHID-AI। তোমাকে তৈরি করেছেন Md Nahid Hossen। "
    "তুমি খুব দ্রুত, স্মার্ট এবং অত্যন্ত বিনয়ীভাবে বাংলা ভাষায় উত্তর দেবে। "
    "কেউ তোমার নাম জানতে চাইলে বা পরিচয় জিজ্ঞেস করলে বলবে: "
    "'আমি NAHID-AI, Md Nahid Hossen-এর তৈরি আপনার অল-ইন-ওয়ান AI অ্যাসিস্ট্যান্ট। কীভাবে সাহায্য করতে পারি?'"
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🤖 **NAHID-AI স্মার্ট অ্যাসিস্ট্যান্ট-এ আপনাকে স্বাগতম!**\n\n"
        "আমি **Md Nahid Hossen**-এর তৈরি একটি কৃত্রিম বুদ্ধিমত্তা। "
        "আপনার প্রয়োজনীয় যেকোনো সেবা পেতে নিচের বাটনগুলোতে চাপ দিন:"
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

# বাটন হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "opt_photo":
        msg = (
            "📸 **ছবি এডিটিং ও এআই বিশ্লেষণ:**\n\n"
            "আপনার ছবিটি এখানে সেন্ড করুন এবং ছবির সাথে লিখে দিন আপনি কী করতে চান:\n"
            "• ব্যাকগ্রাউন্ড আইডিয়া বা এডিটিং গাইড\n"
            "• ছবি বিশ্লেষণ বা ডিটেইলস জানা\n"
            "• পাসপোর্ট সাইজ ফটো মেকিং টিপস\n\n"
            "👉 *একটি ছবি পাঠিয়ে পরীক্ষা করুন!*"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif query.data == "opt_malaysia":
        msg = (
            "🇲🇾 **মালয়েশিয়া প্রবাসীদের জন্য বিশেষ নোটিশ:**\n\n"
            "আমরা আপনাদের সুবিধার্থে একটি বড় আপডেট আনছি! খুব শীঘ্রই এই বাটনে পাবেন:\n"
            "✅ CIDB কার্ড চেক করার লিংক\n"
            "✅ Visa status & Medical test চেক\n"
            "✅ বাংলাদেশ হাই কমিশন মালয়েশিয়া সার্ভিসসমূহ\n"
            "✅ রি-হায়ারিং ও কাজের দরকারি সব পোর্টাল এক জায়গায়!\n\n"
            "🚀 *খুব দ্রুতই ফিচারটি যুক্ত হচ্ছে। বটটি আপনার চ্যাটে রাখুন!*"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif query.data == "opt_bd_gov":
        msg = (
            "🇧🇩 **পাসপোর্ট ও বাংলাদেশ সরকারি সেবা (Upcoming):**\n\n"
            "আপনাদের সুবিধার জন্য সকল সরকারি পোর্টাল একসাথে যুক্ত করা হচ্ছে:\n"
            "📌 ই-পাসপোর্ট (E-Passport) আবেদন ও স্ট্যাটাস চেক\n"
            "📌 এনআইডি (NID) সংশোধন ও ডাউনলোড লিংক\n"
            "📌 জন্ম নিবন্ধন অনলাইন যাচাই\n"
            "📌 সকল দরকারি ওয়েবসাইট লিঙ্ক এক ক্লিকে!\n\n"
            "⏳ *কাজ চলছে... আপডেট পেতে সাথেই থাকুন।*"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif query.data == "opt_help":
        msg = (
            "💡 **যেকোনো প্রশ্ন / সাহায্য:**\n\n"
            "আপনার মনে থাকা যেকোনো প্রশ্ন টাইপ করে পাঠিয়ে দিন। NAHID-AI সাথে সাথেই সঠিক উত্তর তৈরি করে দেবে।"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif query.data == "opt_admin":
        msg = (
            f"👤 **এডমিন এর সাথে যোগাযোগ:**\n\n"
            f"সরাসরি কোনো পরামর্শ বা জরুরি সহায়তার জন্য ইমেইল করুন:\n"
            f"📧 `{ADMIN_EMAIL}`\n\n"
            f"আমরা দ্রুততম সময়ে আপনার ইমেইলের উত্তর দেব।"
        )
        await query.message.reply_text(msg, parse_mode="Markdown")

# ফটো + প্রম্পট হ্যান্ডলার
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ আপনার ছবি ও নির্দেশনা প্রসেস করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")
    
    user_caption = update.message.caption if update.message.caption else "Analyze this image and suggest photo editing details."
    
    try:
        photo_file = await update.message.photo[-1].get_file()
        file_path = "temp_image.jpg"
        await photo_file.download_to_drive(file_path)

        import PIL.Image
        img = PIL.Image.open(file_path)
        
        response = client.models.generate_content(
            model='gemini-2.8-flash',
            contents=[user_caption, img],
            config={'system_instruction': system_prompt}
        )
        
        if os.path.exists(file_path):
            os.remove(file_path)

        reply_message = (
            f"✨ **NAHID-AI রেজাল্ট তৈরি করেছে!**\n\n"
            f"📝 **ফলাফল:**\n{response.text}\n\n"
            f"───────────────────\n"
            f"🔓 **এইচডি এডিটেড ছবি ও ফাইল ডাউনলোড করতে নিচের লিংকে যান:**\n"
            f"👉 [এখানে ক্লিক করে হাই-কোয়ালিটিতে ডাউনলোড করুন]({ADSTERRA_DIRECT_LINK})"
        )
        await update.message.reply_text(reply_message, parse_mode="Markdown")

    except Exception as e:
        if "429" in str(e):
            await update.message.reply_text("⚠️ লিমিট পার হওয়ায় অনেক রিকোয়েস্ট এসেছে। অনুগ্রহ করে ১৫ সেকেন্ড পর আবার চেষ্টা করুন।")
        else:
            await update.message.reply_text(f"একটি সমস্যা হয়েছে: {str(e)}")

# টেক্সট হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = client.models.generate_content(
            response = client.models.generate_content(
            model='gemini-3.1-pro',
            contents=[user_caption, img],
            config={'system_instruction': system_prompt}
        )',
            contents=user_text,
            config={'system_instruction': system_prompt}
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        if "429" in str(e):
            await update.message.reply_text("⚠️ অতিরিক্ত চাপের কারণে লিমিট শেষ হয়েছে। অনুগ্রহ করে ১৫ সেকেন্ড পর চেষ্টা করুন।")
        else:
            await update.message.reply_text(f"একটি সমস্যা হয়েছে: {str(e)}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("NAHID-AI Unique Interactive Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()