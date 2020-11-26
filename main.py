import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import toml
import sqlite3


config = toml.load("config.toml")
group_data = toml.load("list.toml")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
bot_token = config["bot"]["key"]

def make_group(update, context):

    conn = sqlite3.connect('group.db')
    c = conn.cursor()
    msplit = update.message.text.split(' ',2)
    try:
        lmsplit = len(msplit)
        if lmsplit==1:
            return update.message.reply_text("group name not supplied")
        elif lmsplit==2:
            subgroup_name = msplit[1]
            sql_str = f"""insert into groups(group_name) values('{subgroup_name}')"""
        else:
            subgroup_name = msplit[1]
            subgroup_desciption = msplit[2]
            sql_str = f"""insert into groups values('{subgroup_name}','{subgroup_desciption}')"""

        cursor = c.execute(sql_str)
        conn.commit()
        conn.close()
        return update.message.reply_text("group created successfully!")
    except:
        return update.message.reply_text("Group Creation Failed")

def add(update, context):
    try:
        conn = sqlite3.connect('group.db')
        c = conn.cursor()
        subgroup_name = update.message.text.split()[1]
        frm = update.message.reply_to_message.to_dict()

        user_id = frm['from']['id']
        name = frm['from']['first_name']

        query = f"""select group_name from groups where group_name = "{subgroup_name}";"""
        cursor = c.execute(query)
        result = cursor.fetchall()
        if len(result) > 0:
            query = f"""insert into members values('{subgroup_name}','{user_id}','{name}')"""
            cursor = c.execute(query)
            update.message.reply_text(f"successfully added {name} to the group {subgroup_name}")

        else:
            update.message.reply_text("Group name not found!")
            conn.close()
        conn.commit()
        conn.close()
    except:
        return update.message.reply_text("failed to add, use /help")




def tag(id, group_name=""):
    #print("in tag")
    if group_name:
        temp = f"Tagged {group_name}\!"
    else:
        temp = "Tagged the specified subgroup!"

    for x in id:
        temp += f"[\u200b](tg://user?id={x})"

    return temp


def admins(update, context):
    group_id = update.message.chat.id
    admins = context.bot.get_chat_administrators(group_id)
    admins_id = [x.user.id for x in admins]
    # print(admins_id)
    # # add this to db
    # print("running tag")
    tag_text = tag(admins_id, group_name="admins of this group")
    update.message.reply_markdown_v2(f'{tag_text}')

def tag_group(update, context):
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

    tag_text = tag(members_id, group_name=subgroup_name)
    update.message.reply_markdown_v2(f'{tag_text}')


def help(update, context):
    """Echo the user message."""

    update.message.reply_markdown_v2("`/tag <group_name>` : tag group of people \n\n"\
                            "`/admins` : tag all the admins \n\n"\
                            "`/make <group_name> <description>` : Create a group and add some description if you want\n\n"\
                            "`/add <group_name>`: reply this to any message of the person you want to add")


def main():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("admins", admins))
    dp.add_handler(CommandHandler("tag", tag_group))
    dp.add_handler(CommandHandler("make", make_group))
    dp.add_handler(CommandHandler("add", add))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
