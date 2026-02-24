
import telebot
import os
import time
from collections import defaultdict
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- Flask Web Server ---
app = Flask('')

@app.route('/')
def home():
    return "Velqorix Bot is Alive 🔥"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Security Data ---
user_messages = defaultdict(list)
banned_words = ["gali1", "gali2", "abuse"]

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔐 Velqorix Security Bot Activated!")

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

    # Anti-Spam
    user_messages[user_id].append(time.time())
    user_messages[user_id] = [t for t in user_messages[user_id] if time.time() - t < 5]

    if len(user_messages[user_id]) > 5:
        bot.restrict_chat_member(chat_id, user_id, until_date=int(time.time()) + 60)
        bot.send_message(chat_id, "🔇 User muted for spam!")

if _name_ == "_main_":
    keep_alive()
    bot.infinity_polling()
