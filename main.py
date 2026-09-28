import os
import asyncio
import logging
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from google import genai


# =========================================================
# CONFIG
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

MY_TELEGRAM_LINK = os.getenv(
    "MY_TELEGRAM_LINK",
    "https://t.me/your_telegram_username"
).strip()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
).strip()


# =========================================================
# GEMINI CLIENT
# =========================================================

client = None

if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        logger.info("Gemini client initialized successfully.")
    except Exception:
        logger.exception("Gemini client initialization failed.")
else:
    logger.warning("GEMINI_API_KEY is not configured.")


# =========================================================
# RENDER HEALTH SERVER
# =========================================================

class HealthCheckHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header(
            "Content-Type",
            "text/plain; charset=utf-8"
        )
        self.end_headers()
        self.wfile.write(b"PROBASHI AI BOT IS ONLINE")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        return


def run_health_server():

    port = int(
        os.getenv("PORT", "10000")
    )

    server = HTTPServer(
        ("0.0.0.0", port),
        HealthCheckHandler
    )

    logger.info(
        "Render health server running on port %s",
        port
    )

    server.serve_forever()


# =========================================================
# TELEGRAM KEYBOARD
# =========================================================

def main_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "🎬 Video Downloader",
                callback_data="downloader"
            )
        ],

        [
            InlineKeyboardButton(
                "📹 YouTube Planner",
                callback_data="youtube"
            )
        ],

        [
            InlineKeyboardButton(
                "🇧🇩 বাংলাদেশ সরকারি সেবা",
                callback_data="government"
            )
        ],

        [
            InlineKeyboardButton(
                "💬 Admin",
                url=MY_TELEGRAM_LINK
            ),

            InlineKeyboardButton(
                "🚀 Features",
                callback_data="features"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# START
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.effective_message:
        return

    name = (
        update.effective_user.first_name
        if update.effective_user
        else "User"
    )

    text = (
        f"হ্যালো {name}! 👋\n\n"
        "🤖 *PROBASHI AI Assistant*\n\n"
        "আপনি আমাকে সরাসরি যেকোনো প্রশ্ন করতে পারেন।\n\n"
        "নিচের মেনু থেকেও বিভিন্ন সার্ভিস দেখতে পারবেন।"
    )

    await update.effective_message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )


# =========================================================
# HELP
# =========================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.effective_message:
        return

    await update.effective_message.reply_text(
        "আপনার প্রয়োজন অনুযায়ী নিচের মেনু ব্যবহার করুন:",
        reply_markup=main_keyboard()
    )


# =========================================================
# BUTTON HANDLER
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if not query:
        return

    await query.answer()

    if query.data == "downloader":

        text = (
            "🎬 *Social Media Video Downloader*\n\n"
            "এই ফিচারটি বর্তমানে প্রস্তুত করা হচ্ছে।\n\n"
            "পরিকল্পিত সাপোর্ট:\n"
            "• Facebook Video & Reels\n"
            "• TikTok\n"
            "• Instagram Reels\n"
            "• YouTube Shorts\n\n"
            "⏳ Status: Coming Soon"
        )

    elif query.data == "youtube":

        text = (
            "📹 *YouTube Video Planner*\n\n"
            "পরিকল্পিত ফিচার:\n"
            "• Video Ideas\n"
            "• Full Script\n"
            "• SEO Title\n"
            "• Description\n"
            "• Tags\n"
            "• AI Video Prompt\n\n"
            "⏳ Status: Coming Soon"
        )

    elif query.data == "government":

        text = (
            "🇧🇩 *বাংলাদেশ সরকারি সেবা*\n\n"

            "🛂 *E-Passport*\n"
            "https://www.epassport.gov.bd/\n\n"

            "🆔 *NID Service*\n"
            "https://services.nidw.gov.bd/\n\n"

            "🌐 *Bangladesh National Portal*\n"
            "https://bangladesh.gov.bd/\n\n"

            "📑 *Birth Registration*\n"
            "https://bdris.gov.bd/"
        )

    elif query.data == "features":

        text = (
            "🚀 *PROBASHI AI ROADMAP*\n\n"

            "🟢 Version 1.0\n"
            "• Gemini AI Chat\n"
            "• Government Links\n\n"

            "🟡 Version 2.0\n"
            "• Video Downloader\n"
            "• Passport Helper\n\n"

            "🔵 Version 3.0\n"
            "• YouTube Planner\n"
            "• AI Image Tools\n\n"

            "🟣 Future\n"
            "• Automated Tools\n"
            "• More AI Features"
        )

    else:

        text = "এই অপশনটি বর্তমানে পাওয়া যাচ্ছে না।"

    await query.message.reply_text(
        text,
        disable_web_page_preview=True,
        reply_markup=main_keyboard()
    )


# =========================================================
# GEMINI FUNCTION
# =========================================================

def generate_ai_response(prompt):

    if not client:
        raise RuntimeError(
            "GEMINI_API_KEY is missing."
        )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    result = getattr(
        response,
        "text",
        None
    )

    if not result:
        return "দুঃখিত, Gemini কোনো উত্তর দিতে পারেনি।"

    return result.strip()


# =========================================================
# MESSAGE HANDLER
# =========================================================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    prompt = update.message.text.strip()

    if not prompt:
        return

    waiting = await update.message.reply_text(
        "🤖 AI উত্তর তৈরি করছে...\n"
        "একটু অপেক্ষা করুন।"
    )

    try:

        answer = await asyncio.to_thread(
            generate_ai_response,
            prompt
        )

        # Telegram message size protection
        max_length = 4000

        if len(answer) <= max_length:

            await waiting.edit_text(
                answer
            )

        else:

            first_part = answer[:max_length]

            await waiting.edit_text(
                first_part
            )

            remaining = answer[max_length:]

            while remaining:

                part = remaining[:max_length]

                await update.message.reply_text(
                    part
                )

                remaining = remaining[max_length:]

    except Exception:

        logger.exception(
            "Gemini request failed."
        )

        await waiting.edit_text(
            "❌ দুঃখিত!\n\n"
            "AI সার্ভারে বর্তমানে সমস্যা হচ্ছে। "
            "কিছুক্ষণ পরে আবার চেষ্টা করুন।"
        )


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(
    update,
    context
):

    logger.exception(
        "Telegram error: %s",
        context.error
    )


# =========================================================
# MAIN
# =========================================================

def main():

    if not TELEGRAM_BOT_TOKEN:

        logger.critical(
            "TELEGRAM_BOT_TOKEN is missing."
        )

        raise SystemExit(1)

    if not GEMINI_API_KEY:

        logger.warning(
            "GEMINI_API_KEY is missing."
        )

    # Start Render HTTP health server
    Thread(
        target=run_health_server,
        daemon=True
    ).start()

    # Telegram application
    application = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )

    application.add_handler(
        CommandHandler(
            "features",
            help_command
        )
    )

    # Buttons
    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    # Normal messages
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "PROBASHI AI Telegram Bot started."
    )

    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()