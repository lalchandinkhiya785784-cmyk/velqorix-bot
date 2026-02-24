import telebot
import os

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔐 Velqorix Security Bot Activated!")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "Available Commands:\n/start\n/help")

bot.polling()
