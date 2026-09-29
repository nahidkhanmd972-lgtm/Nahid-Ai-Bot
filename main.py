import logging
from google import genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ------------------------------------------------------------------
# আপনার API Keys ও Token এখানে বসাবেন
# ------------------------------------------------------------------
TELEGRAM_BOT_TOKEN = ""
GEMINI_API_KEY = ""
# ------------------------------------------------------------------

# কাস্টম টেক্সট রেসপন্স
WEBSITE_LINKS = {
    "হেল্প": "আপনাকে কীভাবে সাহায্য করতে পারি বলুন?",
    "ওয়েবসাইট": "আমাদের ওয়েবসাইট ভিজিট করুন।",
}

client = genai.Client(api_key=GEMINI_API_KEY)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

SYSTEM_INSTRUCTION = """
তুমি নাহিদের তৈরি করা একটি স্মার্ট এআই অ্যাসিস্ট্যান্ট। 
ইউজারদের প্রশ্নের উত্তর বিনয়ের সাথে ও সংক্ষেপে বাংলায় দেবে।
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text(
        f"হ্যালো {update.effective_user.first_name}! 👋\nআমি নাহিদের এআই অ্যাসিস্ট্যান্ট। আমাকে যেকোনো প্রশ্ন করতে পারেন।"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text.strip()
    await update.message.chat.send_action(action="typing")

    found_link = False
    for keyword, link_text in WEBSITE_LINKS.items():
        if keyword.lower() in user_text.lower():
            await update.message.reply_text(link_text)
            found_link = True
            break

    if not found_link:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_text,
                config={"system_instruction": SYSTEM_INSTRUCTION},
            )
            if response and response.text:
                await update.message.reply_text(response.text)
            else:
                await update.message.reply_text("দুঃখিত, কোনো উত্তর পাওয়া যায়নি।")
        except Exception as e:
            logging.error(f"Error: {e}")
            await update.message.reply_text("এআই রেসপন্স দিতে সমস্যা হচ্ছে।")


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("✅ বট সফলভাবে চালু হয়েছে এবং কাজ করছে...")
    app.run_polling()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("বট বন্ধ করা হয়েছে।")