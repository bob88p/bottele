import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes,MessageHandler , filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", "80"))


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"👋 أهلاً {user.first_name}!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🆘 اكتب أي حاجة وهرد عليك!")


async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"📩 قولت: {text}")


def main():
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN not found in environment variables!")
    
    if not WEBHOOK_URL:
           raise ValueError("❌ WEBHOOK_URL not found! Webhook bots require a public URL.")
    

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

    webhook_path = "/telegram"
    clean_webhook_url = WEBHOOK_URL.rstrip('/')
    full_webhook_url = f"{clean_webhook_url}{webhook_path}"

    logger.info(f"Starting webhook on port {PORT}")
    logger.info(f"Webhook URL: {full_webhook_url}")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=full_webhook_url,
        url_path="telegram",
    )


if __name__ == "__main__":
    main()