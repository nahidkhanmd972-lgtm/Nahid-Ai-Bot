import os
import logging
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

# Logging সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Render Environment Variables থেকে API Key সংগ্রহ
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# আপনার টেলিগ্রাম যোগাযোগের লিংক
MY_TELEGRAM_LINK = "https://telegram.org/dl"

# Gemini Client তৈরি
client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    logging.error("GEMINI_API_KEY পাওয়া যায়নি!")

# মূল ইনলাইন কিবোর্ড/বাটন তৈরি
def get_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🚀 সকল ভার্সন ও ফিচারসমূহ", callback_data="show_features"),
            InlineKeyboardButton("💬 কথা বলতে ক্লিক করুন", url=MY_TELEGRAM_LINK)
        ],
        [
            InlineKeyboardButton("🤖 আমাদের ২য় বটের আপডেট (Coming Soon)", callback_data="next_bot")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# /start কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    welcome_text = (
        f"হ্যালো {user}! 👋\n\n"
        f"আমি Gemini AI চালিত আপনার পার্সোনাল অ্যাসিস্ট্যান্ট বট।\n"
        f"আপনি আমাকে যেকোনো প্রশ্ন করতে পারেন।\n\n"
        f"নিচের বাটনগুলো ব্যবহার করে আমাদের আগামী ফিচারসমূহ ও যোগাযোগ সম্পর্কে জানতে পারেন:"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard())

# /contact বা /features কমান্ড
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"আমাদের সাথে যোগাযোগ করতে বা বিস্তারিত জানতে নিচের বাটনগুলো ব্যবহার করুন:",
        reply_markup=get_main_keyboard()
    )

# বাটন ক্লিকের রেসপন্স (Callback Queries)
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_features":
        features_text = (
            "✨ *আমাদের প্ল্যাটফর্মের ভার্সন ও ভবিষ্যৎ ফিচারসমূহ:* ✨\n\n"
            "🔹 *Version 1.0 (Current):* Gemini AI Chat & Fast Support\n"
            "🔹 *Version 2.0 (Upcoming):* Image Generator & Vision AI\n"
            "🔹 *Version 3.0 (Upcoming):* Voice Message Converter & Automation\n\n"
            "📢 *বিশেষ বার্তা:* আমাদের এই ফিচারগুলো অত্যন্ত শীঘ্রই চালু হতে যাচ্ছে, শুধুমাত্র আপনাদের সেরা অভিজ্ঞতা দেওয়ার জন্য! আমাদের সাথেই থাকুন। ❤️"
        )
        await query.message.reply_text(features_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

    elif query.data == "next_bot":
        next_bot_text = (
            "🤖 *আমাদের ২য় বটের আপডেট:* \n\n"
            "আমরা আরও একটি অ্যাডভান্সড বটের ওপর কাজ করছি যা খুব শীঘ্রই আপনাদের সামনে আনা হবে। "
            "আপনাদের জন্য আমরা সব ধরনের ফিচার এক ছাদের নিচে নিয়ে আসছি!"
        )
        await query.message.reply_text(next_bot_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

# মেসেজ প্রসেসিং ও Gemini AI রেসপন্স
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    
    # ইউজার যদি কথা বলার ইচ্ছা বা ফিচারের কথা প্রকাশ করে
    contact_keywords = ["কথা বলতে চাই", "contact", "owner", "admin", "যোগাযোগ", "feature", "ফিচার", "version"]
    if any(keyword in user_prompt.lower() for keyword in contact_keywords):
        await update.message.reply_text(
            "নিচের মেনু থেকে আপনার পছন্দমতো অপশনটি বেছে নিন:",
            reply_markup=get_main_keyboard()
        )
        return

    # ইউজারকে অপেক্ষমাণ বার্তা পাঠানো
    sent_message = await update.message.reply_text("প্রসেস করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")

    try:
        if not client:
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=sent_message.message_id,
                text="Gemini API Key সেটআপ করা নেই।"
            )
            return

        # নতুন google-genai SDK দিয়ে রেসপন্স তৈরি
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt
        )
        ai_reply = response.text

        # টেলিগ্রামে উত্তর পাঠানো
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

def main():
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN পাওয়া যায়নি!")
        return

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # হ্যান্ডলার যুক্ত করা
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("features", contact))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot চালিত হচ্ছে...")
    app.run_polling()

if __name__ == '__main__':
    main()