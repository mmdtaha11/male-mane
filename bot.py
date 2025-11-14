import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# --- تنظیمات اولیه ---
BOT_TOKEN = "7440922727:AAEMmpc3V-wvHDifg9uCV4h0mXxk_IqIqh4"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    """فقط به /start جواب می‌دهد"""
    update.message.reply_text('سلام! ربات تست ساده من کار می‌کند!')

def main():
    """ربات را اجرا می‌کند"""
    try:
        updater = Updater(BOT_TOKEN, use_context=True)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", start))

        print("--- ربات تست ساده (نسخه قدیمی) با موفقیت در حال اجراست ---")
        logger.info("--- ربات تست ساده (نسخه قدیمی) با موفقیت در حال اجراست ---")

        updater.start_polling()
        updater.idle()

    except Exception as e:
        # اگر ربات کرش کند، خطا را چاپ می‌کند
        print("!!!!!!!!!!!!!!!!! خطای بحرانی !!!!!!!!!!!!!!!!!!")
        print(f"ربات به دلیل این خطا اجرا نشد: {e}")
        logger.error("ربات به دلیل این خطا اجرا نشد:", exc_info=True)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

if __name__ == "__main__":
    main()
