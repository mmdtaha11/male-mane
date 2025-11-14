import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- ✨ توکن شما اینجاست ---
BOT_TOKEN = "7440922727:AAEMmpc3V-wvHDifg9uCV4h0mXxk_IqIqh4"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """فقط به /start جواب می‌دهد"""
    await update.message.reply_text('سلام! ربات تست من کار می‌کند!')

def main():
    """ربات را اجرا می‌کند"""
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        print("--- ربات تست با موفقیت در حال اجراست ---")
        application.run_polling()
    except Exception as e:
        # --- ✨ اگر ربات کرش کند، خطا را چاپ می‌کند ---
        print("!!!!!!!!!!!!!!!!! خطای بحرانی !!!!!!!!!!!!!!!!!!")
        print(f"ربات به دلیل این خطا اجرا نشد: {e}")
        logger.error("ربات به دلیل این خطا اجرا نشد:", exc_info=True)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

if __name__ == "__main__":
    main()
