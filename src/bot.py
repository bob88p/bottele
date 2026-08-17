import os
import logging
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)


load_dotenv()

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Get token from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", "8080"))


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 أهلاً {user.first_name}!\n\n"
        f"أنا بوت بسيط بيعرف:\n"
        f"• /start — الترحيب\n"
        f"• /help — المساعدة\n"
        f"• أي رسالة — يرد عليك"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    await update.message.reply_text(
        "🆘 المساعدة:\n\n"
        "• اكتب أي حاجة — هرد عليك\n"
        "• البوت شغال 24/7!"
    )


async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo any text message back."""
    text = update.message.text
    await update.message.reply_text(f"📩 قولت: {text}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors."""
    logger.error(f"Update {update} caused error: {context.error}")


def main() -> None:
    """Start the bot."""
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not found! Add it to .env file.")

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

    # Add error handler
    application.add_error_handler(error_handler)
    webhook_path = "/telegram"
    full_webhook_url = f"{WEBHOOK_URL}{webhook_path}"
    # Set webhook
    await application.bot.set_webhook(full_webhook_url)
    logger.info(f"✅ Webhook set to: {full_webhook_url}")


    # Run the bot (webhook)
    logger.info("🚀 Bot is starting...")
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="telegram",
        webhook_url=full_webhook_url,
    )


if __name__ == "__main__":
    main()