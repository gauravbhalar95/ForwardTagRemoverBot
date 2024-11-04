import logging
import os
from flask import Flask, request
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask application setup
app = Flask(__name__)

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Config class to hold constants
class Config:
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", None)  # Add your webhook URL here
    SOURCE = "https://github.com/Artis7eeR/ForwardTagRemoverBot"
    START_TEXT = """
Hi [{}](tg://user?id={}) 
I am A Forward Tag remover Bot.
Send /help to know more ©[Abdul Razaq](https://github.com/artis7eer)"""
    HELP_TEXT = "Forward Me A File, Video, Audio, Photo, or Anything And \nI will Send You the File Back\n\n`How to Set Caption?`\nReply Caption to a File, Photo, Audio, Media"

# Handlers
async def startMessage(update, context):
    await update.message.reply_text(Config.START_TEXT.format(update.effective_user.first_name, update.effective_user.id))

async def helpMessage(update, context):
    await update.message.reply_text(Config.HELP_TEXT)

async def handleCaption(update, context):
    # Handle message with caption
    await update.message.reply_text("Caption received!")

async def handleMessage(update, context):
    # Handle other messages
    await update.message.reply_text("Message received!")

# Flask route for webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    json_update = request.get_json()
    bot.update_queue.put(json_update)  # Assuming `bot` has an `update_queue`
    return "OK"

def main():
    # Initialize the bot
    global bot  # Make `bot` accessible in the webhook function
    bot = ApplicationBuilder().token(Config.BOT_TOKEN).build()
    
    # Add command and message handlers
    bot.add_handler(CommandHandler('start', startMessage))
    bot.add_handler(CommandHandler('help', helpMessage))
    bot.add_handler(MessageHandler(filters.REPLY, handleCaption))
    bot.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handleMessage))

    # Set the webhook URL
    bot.bot.set_webhook(url=Config.WEBHOOK_URL)

    # Start the bot
    bot.run_polling()  # This could be replaced by an equivalent function if necessary

    # Start Flask server
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()