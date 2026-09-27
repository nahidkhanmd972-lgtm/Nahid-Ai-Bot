import logging
import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Render Environment Variables থেকে Keys গ্রহণ
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API সেটিং
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.8-flash")

# লগিং কনফিগারেশন
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


# /start কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 **স্বাগতম!**\n\n"
        "আমি **Nahid AI**। আমাকে যেকোনো প্রশ্ন করতে পারেন, আমি সাহায্য করার জন্য প্রস্তুত।\n\n"
        "💡 সাহায্য পেতে /help টাইপ করুন।"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


# /help কমান্ড হ্যান্ডলার
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "❓ **কীভাবে ব্যবহার করবেন:**\n\n"
        "১. চ্যাট বক্সে যেকোনো প্রশ্ন টাইপ করে পাঠিয়ে দিন।\n"
        "২. Nahid AI সাথে সাথে আপনার প্রশ্নের উত্তর তৈরি করে দেবে।\n"
        "৩. নতুন চ্যাট শুরু করতে /start লিখুন।"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


# সাধারণ মেসেজ এবং AI উত্তর হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"একটি সমস্যা হয়েছে: {str(e)}")


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # কমান্ড হ্যান্ডলার যোগ করা
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # সাধারণ টেক্সট মেসেজ হ্যান্ডলার যোগ করা
    app.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    )

    print("Nahid AI Bot is running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
