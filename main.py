import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Logging সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Render Environment Variables থেকে API Key সংগ্রহ
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")  # Render-এ "TELEGRAM_BOT_TOKEN" নামে সেট করবেন
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")          # Render-এ "GEMINI_API_KEY" নামে সেট করবেন

# Gemini AI কনফিগারেশন
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    logging.error("GEMINI_API_KEY পাওয়া যায়নি!")

# /start কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(f"হ্যালো {user}! আমি Gemini AI চালিত একটি টেলিগ্রাম বট। আমাকে যেকোনো প্রশ্ন করতে পারেন।")

# মেসেজ প্রসেসিং ও Gemini AI রেসপন্স
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    
    # ইউজারকে অপেক্ষমাণ বার্তা পাঠানো
    sent_message = await update.message.reply_text("প্রসেস করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")

    try:
        if not GEMINI_API_KEY:
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=sent_message.message_id,
                text="Gemini API Key সেটআপ করা নেই।"
            )
            return

        # Gemini AI থেকে উত্তর চাওয়া
        response = model.generate_content(user_prompt)
        ai_reply = response.text

        # টেলিগ্রামে উত্তর আপডেট করে পাঠানো
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=sent_message.message_id,
            text=ai_reply
        )
    except Exception as e:
        logging.error(f"Error: {e}")
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=sent_message.message_id,
            text="দুঃখিত, কোনো একটি সমস্যা হয়েছে। আবার চেষ্টা করুন।"
        )

# প্রধান রানার ফাংশন
def main():
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN পাওয়া যায়নি!")
        return

    # Telegram Bot অ্যাপ্লিকেশন তৈরি
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # হ্যান্ডলার যুক্ত করা
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot চালিত হচ্ছে...")
    app.run_polling()

if __name__ == '__main__':
    main()