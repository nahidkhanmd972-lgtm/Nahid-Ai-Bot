import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# এনভায়রনমেন্ট থেকে টোকেন ও এপিআই কি নেওয়া
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("TELEGRAM_BOT_TOKEN অথবা GEMINI_API_KEY সেট করা নেই!")

# গুগল জেমিনি ক্লায়েন্ট ইনিশিয়ালাইজেশন (নতুন google-genai এসডিকে অনুযায়ী)
client = genai.Client(api_key=GEMINI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.effective_user.first_name
    
    logging.info(f"Message from {user_name}: {user_message}")
    
    try:
        # জেমিনি মডেল থেকে রেসপন্স নেওয়া (flash মডেল ব্যবহার করা হয়েছে)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        reply_text = response.text
    except Exception as e:
        logging.error(f"Error generating AI response: {e}")
        reply_text = "দুঃখিত, এই মুহূর্তে জেমিনি এপিআই থেকে উত্তর আনতে সমস্যা হচ্ছে।"

    await update.message.reply_text(reply_text)

def main():
    # টেলিগ্রাম বট অ্যাপ্লিকেশন তৈরি
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # টেক্সট মেসেজ হ্যান্ডলার যোগ করা
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("বট সফলভাবে চালু হয়েছে এবং কাজ করছে...")
    # বট রান করা (Polling মেথড)
    application.run_polling()

if __name__ == '__main__':
    main()