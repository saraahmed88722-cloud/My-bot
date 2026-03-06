import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# 1. نظام الحماية للبقاء حياً على Render
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run).start()

# 2. إعدادات البوت (التوكن الخاص بك)
API_TOKEN = '8629591404:AAElD9enpGE52EH8DNaNVeLJp14cU9eD64o'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("📐 الرياضيات", callback_data="math")
    btn2 = types.InlineKeyboardButton("📖 اللغة العربية", callback_data="arabic")
    btn3 = types.InlineKeyboardButton("🧪 الفيزياء", callback_data="physics")
    markup.add(btn1, btn2, btn3)
    
    bot.reply_to(message, f"📚 مرحباً {message.from_user.first_name} في بوت الشهادة السودانية.\nاختر المادة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "math":
        bot.answer_callback_query(call.id, "جاري تجهيز امتحانات الرياضيات...")
        bot.send_message(call.message.chat.id, "📝 إليك روابط امتحانات الرياضيات: [رابط الملف هنا]")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
