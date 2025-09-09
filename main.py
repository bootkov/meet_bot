import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import dotenv_values
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    filename='logs/bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

config = dotenv_values(".env")

# Your bot token from @BotFather
BOT_TOKEN = config["TOKEN"]
TRIGGER_PHRASE = config["TRIGGER_PHRASE"]
ALLOWED_CHANNEL_ID = int(config["ALLOWED_CHANNEL_ID"])
URL = config["URL"]

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle channel posts from a specific channel."""

    if update.channel_post.chat.id != ALLOWED_CHANNEL_ID:
        logging.error(f'Message from unknown channel: {update.channel_post.chat.id}')
        return

    message_text = update.channel_post.text.lower() if update.channel_post and update.channel_post.text else ""

    # Only respond if message contains the trigger phrase
    if TRIGGER_PHRASE.lower() in message_text:
        # Create inline keyboard with URL button
        keyboard = [
            [InlineKeyboardButton("Google Meet", url=URL)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.channel_post.reply_text(
            "☎️",
            reply_markup=reply_markup
        )

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handler for regular messages (private chats, groups)
    application.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, handle_channel_post))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()