import logging
import os
from telegram.ext import (
    filters,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler
)
from flask import Flask, request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configuration class to store bot settings
class Config:
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # Your webhook URL
    START_TEXT = """
Hi [{}](tg://user?id={}) 
I am A Forward Tag remover Bot.
Send /help to know more ©[Abdul Razaq](https://github.com/artis7eer)"""
    HELP_TEXT = "Forward Me A File, Video, Audio, Photo, or Anything And \nI will Send You the File Back\n\n`How to Set Caption?`\nReply Caption to a File, Photo, Audio, Media"

# Flask route for receiving updates from Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    json_update = request.get_json()
    logging.info(f"Received update: {json_update}")  # Log the incoming update
    bot.update_queue.put(json_update)
    return "OK"

# Health check endpoint for monitoring
@app.route('/health', methods=['GET'])
def health_check():
    return "Healthy", 200

# Command handler functions
def startMessage(update, context):
    """Send a welcome message when the command /start is issued."""
    user_first_name = update.message.from_user.first_name
    user_id = update.message.from_user.id
    update.message.reply_text(Config.START_TEXT.format(user_first_name, user_id))

def helpMessage(update, context):
    """Send help information when the command /help is issued."""
    update.message.reply_text(Config.HELP_TEXT)

def handleCaption(update, context):
    """Handle messages that include a caption."""
    update.message.reply_text("Caption received!")

def handleMessage(update, context):
    """Handle general messages without specific filters."""
    update.message.reply_text("Message received!")

def main():
    global bot
    # Initialize the bot with the given token
    bot = ApplicationBuilder().token(Config.BOT_TOKEN).build()
    # Register command and message handlers
    bot.add_handler(CommandHandler('start', startMessage))
    bot.add_handler(CommandHandler('help', helpMessage))
    bot.add_handler(MessageHandler(filters.REPLY, handleCaption))
    bot.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handleMessage))

    # Set the webhook URL
    bot.bot.set_webhook(url=Config.WEBHOOK_URL)

    # Start Flask server
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()