import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import toml

config = toml.load("config.toml")
group_data = toml.load("list.toml")
# /add [string] [username] -> to add a user to a group
# /make [string] -> to make a new group
# /tag [string] -> to tag a group of people


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
bot_token = config["bot"]["key"]

def tag(id, group_name=""):
    print("in tag")
    if group_name:
        temp = f"Tagged {group_name}\!"
    else:
        temp = "Tagged the specified subgroup!"

    for x in id:
        temp += f"[\u200b](tg://user?id={x})"
    
    return temp


def tag_admin(update, context):
    group_id = update.message.chat.id
    admins = context.bot.get_chat_administrators(group_id)
    admins_id = [x.user.id for x in admins]
    print(admins_id)
    # add this to db 
    print("running tag")
    tag_text = tag(admins_id, group_name="admins of OT")
    update.message.reply_markdown_v2(f'{tag_text}')

def tag_a_group(update, context):
    """Send a message when the command /help is issued."""
    try:
        subgroup_name = update.message.text.split()[1]
    except:
        return update.message.reply_text("Also send a group name!")

    # TODO alok
    # if not somesqlmagic.search(subgroup_name):
    #     return update.message.reply_text("The group doesn't exist!")

    # temp = ""
    # for x in somesqlmagic.filter(subgroup_name):
    #     temp += f"[\u200b](tg://user?id={x})"
    # update.message.reply_markdown_v2(f'Tagged {group} {temp}')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(bot_token, use_context=True)
    print("Working lol")
    dp = updater.dispatcher
    # dp.add_handler(CommandHandler("meow", meow_command))
    dp.add_handler(CommandHandler("meow", tag_admin))
    dp.add_handler(CommandHandler("echo", echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
