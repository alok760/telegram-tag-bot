import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import toml
import sqlite3


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

def make(update, context):

    conn = sqlite3.connect('group.db')
    c = conn.cursor()
    try:
        subgroup_name = update.message.text.split()[1]
        subgroup_desciption = update.message.text.split()[2]
    except:
        return update.message.reply_text("Also send a group name!")

    query = f"""insert into groups values('{subgroup_name}','{subgroup_desciption}')"""
    cursor = c.execute(query)
    conn.commit()
    conn.close()
    return update.message.reply_text("group created successfully!")
    #breakpoint()


def add(update, context):

    try:
        subgroup_name = update.message.text.split()[1]
    except:
        return update.message.reply_text("Also send a group name!")

    group_name = "meow"
    user_id = '271397625'


    pass

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
    tag_text = tag(admins_id, group_name="admins of this group")
    update.message.reply_markdown_v2(f'{tag_text}')

def tag_a_group(update, context):
    conn = sqlite3.connect('group.db')
    c = conn.cursor()

    try:
        subgroup_name = update.message.text.split()[1]
    except:
        return update.message.reply_text("Also send a group name!")

    query = f"""select group_name from groups where group_name = "{subgroup_name}";"""
    cursor = c.execute(query)
    result = cursor.fetchall()
    if len(result) > 0:
        query = f"""select member_id from members where group_name = '{subgroup_name}';"""
        mcursor = conn.execute(query)
        res = mcursor.fetchall()
    members_id = [i[0] for i in res]

    tag_text = tag(members_id, group_name="meow group")
    update.message.reply_markdown_v2(f'{tag_text}')




def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    # dp.add_handler(CommandHandler("meow", meow_command))
    dp.add_handler(CommandHandler("admins", tag_admin))
    dp.add_handler(CommandHandler("group", tag_a_group))
    dp.add_handler(CommandHandler("make_group", make))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
