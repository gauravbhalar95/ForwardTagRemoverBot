import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", None)  # Add your webhook URL here
    SOURCE = "https://github.com/Artis7eeR/ForwardTagRemoverBot"
    START_TEXT = """
Hi [{}](tg://user?id={}) 
I am A Forward Tag remover Bot.
Send /help to know more ©[Abdul Razaq](https://github.com/artis7eer)"""
    HELP_TEXT = "Forward Me A File, Video, Audio, Photo, or Anything And \nI will Send You the File Back\n\n`How to Set Caption?`\nReply Caption to a File, Photo, Audio, Media"