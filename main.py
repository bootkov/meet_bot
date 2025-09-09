import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import dotenv_values
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(
    filename='logs/bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

config = dotenv_values(".env")
BOT_TOKEN = config["TOKEN"]
TRIGGER_PHRASE = config["TRIGGER_PHRASE"]
ALLOWED_GROUP_ID = int(config["ALLOWED_GROUP_ID"])
URL = config["URL"]

async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    
    if update.message.chat.id != ALLOWED_GROUP_ID:
        logging.error(f'Message from unknown group: {update.message.chat.id}')
        return
    
    message_text = update.message.text.lower() if update.message and update.message.text else ""
    
    if TRIGGER_PHRASE.lower() in message_text:
        keyboard = [
            [InlineKeyboardButton("Google Meet", url=URL)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "☎️",
            reply_markup=reply_markup
        )

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(MessageHandler(
        filters.TEXT, 
        handle_group_message
    ))
    
    application.run_polling(allowed_updates=Update.MESSAGE)

if __name__ == '__main__':
    main()