import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
bot_token = os.environ['bot_token']

def meow_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_markdown_v2('@admin [\u200b](tg://user?id=123123123)')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def main():

    updater = Updater(bot_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("meow", meow_command))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
