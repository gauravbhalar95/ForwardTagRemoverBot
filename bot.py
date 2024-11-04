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

app = Flask(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Flask route for webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    json_update = request.get_json()
    bot.update_queue.put(json_update)
    return "OK"

def main():
    bot = ApplicationBuilder().token(Config.BOT_TOKEN).build()
    bot.add_handler(CommandHandler('start', startMessage))
    bot.add_handler(CommandHandler('help', helpMessage))
    bot.add_handler(MessageHandler(filters.REPLY, handleCaption))
    bot.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handleMessage))

    # Set the webhook URL
    bot.bot.set_webhook(url=Config.WEBHOOK_URL)

    # Start Flask server
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()