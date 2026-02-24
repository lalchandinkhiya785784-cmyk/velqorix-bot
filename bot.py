import telebot
import os
import time
from collections import defaultdict

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Track user messages for anti-spam
user_messages = defaultdict(list)

# Banned words list
banned_words = ["gali1", "gali2", "abuse"]

# 🔹 START
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔐 Velqorix Security Bot Activated!")

# 🔹 HELP
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "/ban /mute /unban\nAuto link delete enabled.")

# 🔹 AUTO DELETE LINKS
@bot.message_handler(func=lambda m: True)
def security_check(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text.lower() if message.text else ""

    # Anti-Link
    if "http" in text or "t.me" in text:
        bot.delete_message(chat_id, message.message_id)
        bot.send_message(chat_id, "🚫 Links are not allowed!")
        return

    # Abuse Filter
    for word in banned_words:
        if word in text:
            bot.delete_message(chat_id, message.message_id)
            bot.send_message(chat_id, "⚠️ Abuse is not allowed!")
            return

    # Anti-Spam (5 messages in 5 seconds)
    user_messages[user_id].append(time.time())
    user_messages[user_id] = [t for t in user_messages[user_id] if time.time() - t < 5]

    if len(user_messages[user_id]) > 5:
        bot.restrict_chat_member(chat_id, user_id, until_date=int(time.time()) + 60)
        bot.send_message(chat_id, "🔇 User muted for spam!")

# 🔹 BAN COMMAND
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.ban_chat_member(message.chat.id, user_id)
        bot.send_message(message.chat.id, "🚫 User banned!")

bot.infinity_polling()
