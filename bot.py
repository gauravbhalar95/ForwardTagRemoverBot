import logging
from telegram.ext import (
    filters,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler
)
from plugins.__main__ import *  # Make sure this imports the necessary functions
from config import Config

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define the message handler
async def handleMessage(update, context):
    logging.info(f'Received update: {update}')
    
    if update.message:
        try:
            # Check if the message is not None and copy it to the user
            await update.message.copy(chat_id=update.effective_user.id)
            logging.info(f'Message copied to user {update.effective_user.id}')
        except Exception as e:
            logging.error(f'Error copying message: {e}')
    else:
        logging.warning('Received an update without a message.')

# Main function to start the bot
def main():
    bot = ApplicationBuilder().token(Config.BOT_TOKEN).build()
    bot.add_handler(CommandHandler('start', startMessage))
    bot.add_handler(CommandHandler('help', helpMessage))
    bot.add_handler(MessageHandler(filters.REPLY, handleCaption))
    bot.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handleMessage))
    
    logging.info('Bot is starting...')
    bot.run_polling()

if __name__ == '__main__':
    main()