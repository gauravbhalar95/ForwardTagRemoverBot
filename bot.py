import logging
from telegram.ext import (
    filters,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler
)
from plugins.__main__ import *
from config import Config
from flask import Flask, request

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Create a Flask app
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Handle the incoming webhook update
    update = request.get_json()
    logging.info(f'Received webhook update: {update}')
    
    application = ApplicationBuilder().token(Config.BOT_TOKEN).build()
    application.process_update(update)  # Process the update from the webhook
    return 'ok', 200

async def handleMessage(update, context):
    logging.info(f'Received update: {update}')
    
    if update.message:
        try:
            await update.message.copy(chat_id=update.effective_user.id)
            logging.info(f'Message copied to user {update.effective_user.id}')
        except Exception as e:
            logging.error(f'Error copying message: {e}')
    else:
        logging.warning('Received an update without a message.')

def main():
    bot = ApplicationBuilder().token(Config.BOT_TOKEN).build()
    bot.add_handler(CommandHandler('start', startMessage))
    bot.add_handler(CommandHandler('help', helpMessage))
    bot.add_handler(MessageHandler(filters.REPLY, handleCaption))
    bot.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handleMessage))

    # Use webhooks for Heroku
    if Config.WEBHOOK_URL:
        bot.run_webhook(listen='0.0.0.0',
                        port=int(os.environ.get('PORT', 8443)),  # Use port from Heroku
                        url_path=Config.BOT_TOKEN)  # Set the url path to the bot token
        logging.info(f'Webhook set to {Config.WEBHOOK_URL}/{Config.BOT_TOKEN}')
    else:
        bot.run_polling()

if __name__ == '__main__':
    main()