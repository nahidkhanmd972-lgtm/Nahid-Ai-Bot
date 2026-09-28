import os
import logging
import asyncio
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler, 
    filters, 
    ContextTypes
)
from google import genai

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# আপনার টেলিগ্রাম ইউজারনেম বা সাপোর্ট লিঙ্ক
MY_TELEGRAM_LINK = "https://t.me/your_telegram_username"

# Gemini Client তৈরি
client = None
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        logging.info("Gemini Client successfully initialized.")
    except Exception as e:
        logging.error(f"Gemini Client error: {e}")
else:
    logging.warning("GEMINI_API_KEY environment variable is not set!")

# Render Health Check Server
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logging.info(f"Health check server running on port {port}")
    server.serve_forever()

# প্রধান ইনলাইন কিবোর্ড মেনু
def get_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🎬 Video Downloader (FB/TikTok/IG)", callback_data="feature_downloader"),
        ],
        [
            InlineKeyboardButton("📹 YouTube Video & Prompt Planner", callback_data="feature_yt_planner")
        ],
        [
            InlineKeyboardButton("🏛️ পাসপোর্ট ও সরকারি ওয়েবসাইট লিঙ্ক", callback_data="feature_gov_links")
        ],
        [
            InlineKeyboardButton("💬 অ্যাডমিনের সাথে কথা বলুন", url=MY_TELEGRAM_LINK),
            InlineKeyboardButton("🚀 ফিউচার আপডেটস ও ভার্সন", callback_data="show_features")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name if update.effective_user else "User"
    welcome_text = (
        f"হ্যালো {user}! 👋\n\n"
        f"আমি **AI Assistant**, আপনার জন্য কি করতে পারি?\n\n"
        f"আপনি আমাকে সরাসরি যেকোনো প্রশ্ন করতে পারেন, অথবা নিচের সুইচগুলো ব্যবহার করে আমাদের আগামী ফিচার ও সার্ভিসসমূহ দেখতে পারেন:"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

# /contact বা হেল্প কমান্ড
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "যোগাযোগ বা আমাদের ফিচারসমূহ ব্যবহারের জন্য নিচের যেকোনো সুইচে ক্লিক করুন:",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

# বাটন ক্লিক হ্যান্ডলার
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "feature_downloader":
        downloader_text = (
            "📥 *Social Media Video Downloader Bot (Coming Soon)* 🎬\n\n"
            "খুব শীঘ্রই এই ফিচারের মাধ্যমে আপনি এক ক্লিকেই ভিডিও ডাউনলোড করতে পারবেন:\n"
            "• Facebook Video & Reels Downloader 🟦\n"
            "• TikTok Watermark-Free Downloader 🎵\n"
            "• Instagram Reels & Post Downloader 📸\n"
            "• YouTube Shorts Downloader 🔴\n\n"
            "⏳ *স্ট্যাটাস:* কাজ চলছে, খুব শীঘ্রই চালু হবে!"
        )
        await query.message.reply_text(downloader_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

    elif query.data == "feature_yt_planner":
        yt_text = (
            "📹 *YouTube Video Planner & Prompt Generator (Coming Soon)* 🚀\n\n"
            "কনটেন্ট ক্রিয়েটরদের জন্য বিশেষ এআই টুল:\n"
            "• ভিডিও আইডিয়া বিশ্লেষণ ও প্ল্যান তৈরি 💡\n"
            "• সম্পূর্ণ ভিডিওর স্ক্রিপ্ট জেনারেটর 📜\n"
            "• SEO টাইটেল, ডেসক্রিপশন ও ট্যাগ তৈরি 🏷️\n"
            "• AI Video Prompt জেনারেটর 🎨\n\n"
            "⏳ *স্ট্যাটাস:* পরবর্তী আপডেটে যুক্ত করা হবে!"
        )
        await query.message.reply_text(yt_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

    elif query.data == "feature_gov_links":
        gov_text = (
            "🏛️ *বাংলাদেশ সরকারি সেবা ও ই-পাসপোর্ট পোর্টাল* 🇧🇩\n\n"
            "সহজেই সরকারি সেবা পেতে নিচের অফিশিয়াল লিঙ্কগুলো ব্যবহার করুন:\n\n"
            "• 🛂 *ই-পাসপোর্ট অনলাইন আবেদন:* [epassport.gov.bd](https://www.epassport.gov.bd/)\n"
            "• 🆔 *এনআইডি সার্ভিস পোর্টাল:* [services.nidw.gov.bd](https://services.nidw.gov.bd/)\n"
            "• 🌐 *জাতীয় তথ্য বাতায়ন:* [bangladesh.gov.bd](https://bangladesh.gov.bd/)\n"
            "• 📑 *জন্ম ও মৃত্যু নিবন্ধন:* [bdris.gov.bd](https://bdris.gov.bd/)\n\n"
            "💡 *দ্রষ্টব্য:* পরবর্তীতে আরও সরকারি সার্ভিস পোর্টাল এখানে যুক্ত করা হবে।"
        )
        await query.message.reply_text(gov_text, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=get_main_keyboard())

    elif query.data == "show_features":
        features_text = (
            "🚀 *আমাদের সকল রোডম্যাপ ও আগামী প্ল্যান:* ✨\n\n"
            "🟢 *Version 1.0 (Active):*\n"
            "• Gemini AI Chat Assistant 💬\n"
            "• Fast Support & Gov Portal Directory 🏛️\n\n"
            "🟡 *Version 2.0 (In Progress):*\n"
            "• Social Media Video Downloader Bot 🎬\n"
            "• Passport & Gov Service Helper 🛂\n\n"
            "🔵 *Version 3.0 (Planned):*\n"
            "• YouTube Video & AI Prompt Planner 📹\n"
            "• HD AI Image Generator 🎨\n\n"
            "🟣 *Version 4.0 (Future Update):*\n"
            "• Direct Admin Support Switch 💬\n"
            "• Automated Tools & Workflows 💻\n\n"
            "📢 যেকোনো প্রশ্ন থাকলে আমাদের অ্যাডমিনের সাথে যোগাযোগ করুন!"
        )
        await query.message.reply_text(features_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

# সাধারণ মেসেজ হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    
    contact_keywords = ["কথা বলতে চাই", "contact", "owner", "admin", "যোগাযোগ", "feature", "ফিচার", "version", "passport", "পাসপোর্ট", "video", "ভিডিও"]
    if any(keyword in user_prompt.lower() for keyword in contact_keywords):
        await update.message.reply_text(
            "আপনার প্রয়োজন অনুযায়ী নিচের সুইচগুলো চাপুন:",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        return

    sent_message = await update.message.reply_text("প্রসেস করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")

    try:
        if not client:
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=sent_message.message_id,
                text="Gemini API Key সেটআপ করা নেই।"
            )
            return

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt
        )
        ai_reply = response.text

        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=sent_message.message_id,
            text=ai_reply
        )
    except Exception as e:
        logging.error(f"Gemini generation error: {e}")
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=sent_message.message_id,
            text="দুঃখিত, কোনো একটি সমস্যা হয়েছে। আবার চেষ্টা করুন।"
        )

def main():
    if not TELEGRAM_BOT_TOKEN:
        logging.critical("CRITICAL ERROR: TELEGRAM_BOT_TOKEN পাওয়া যায়নি! প্রোগ্রাম বন্ধ হচ্ছে।")
        return

    # ডামি ডাব্লিউইবি সার্ভার ব্যাকগ্রাউন্ডে চালু করা
    Thread(target=run_dummy_server, daemon=True).start()

    # টেলিগ্রাম বট অ্যাপ তৈরি
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("features", contact))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot সফলভাবে চালু হয়েছে...")
    app.run_polling()

if __name__ == '__main__':
    main()