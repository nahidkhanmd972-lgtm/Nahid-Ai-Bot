import logging
import google.generativeai as genai
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
    await update.message.reply_text(
        "হ্যালো! আমি আপনার AI অ্যাসিস্ট্যান্ট। আমাকে যেকোনো প্রশ্ন করতে পারেন।"
    )


# টেক্সট মেসেজ এবং Gemini AI দিয়ে উত্তর দেওয়ার হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"একটি সমস্যা হয়েছে: {str(e)}")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    )

    print("Bot is running...")
    app.run_polling()
# কাস্টম টেক্সট রেসপন্স
WEBSITE_LINKS = {
    "হেল্প": "আপনাকে কীভাবে সাহায্য করতে পারি বলুন?",
    "ওয়েবসাইট": "আমাদের ওয়েবসাইট ভিজিট করুন।",
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not update.message:
    return
  await update.message.reply_text(
      f"হ্যালো {update.effective_user.first_name}! 👋\nআমি নাহিদের এআই"
      " অ্যাসিস্ট্যান্ট। আমাকে যেকোনো প্রশ্ন করতে পারেন।"
  )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not update.message or not update.message.text:
    return

  user_text = update.message.text.strip()
  await update.message.chat.send_action(action="typing")

  # ১. কিওয়ার্ড চেক
  found_link = False
  for keyword, link_text in WEBSITE_LINKS.items():
    if keyword.lower() in user_text.lower():
      await update.message.reply_text(link_text)
      found_link = True
      break

  # ২. এআই রেসপন্স
  if not found_link:
    try:
      response = model.generate_content(user_text)
      if response and response.text:
        await update.message.reply_text(response.text)
      else:
        await update.message.reply_text("দুঃখিত, কোনো উত্তর পাওয়া যায়নি।")
    except Exception as e:
      await update.message.reply_text(f"এআই সমস্যা: {e}")


def main():
  app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

  app.add_handler(CommandHandler("start", start))
  app.add_handler(
      MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
  )

  print("✅ বট সফলভাবে চালু হয়েছে এবং কাজ করছে...")
  app.run_polling()


if __name__ == "__main__":
  main()