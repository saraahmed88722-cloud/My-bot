    import telebot
import requests
import os
from flask import Flask
from threading import Thread

# 1. السيرفر الوهمي لمنع توقف Render
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run).start()

# 2. إعدادات البوت
API_TOKEN = '8629591404:AAElD9enpGE52EH8DNaNVeLJp14cU9eD64o'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🌟 البوت شغال بنجاح! أرسل رابط تيك توك الآن.")

@bot.message_handler(func=lambda m: 'tiktok.com' in m.text or 'v.douyin.com' in m.text)
def handle_tiktok(message):
    msg = bot.reply_to(message, "⏳ جاري تجاوز الحظر وجلب الفيديو...")
    try:
        # استخدام API خارجي لتجاوز حظر تيك توك تماماً
        api_url = f"https://api.tiklydown.eu.org/api/download?url={message.text}"
        res = requests.get(api_url).json()
        
        # جلب الرابط المباشر للفيديو بدون علامة مائية
        video_url = res['video']['noWatermark']
        
        # إرسال الفيديو للمستخدم
        bot.send_video(message.chat.id, video_url, caption="✅ تم التحميل بنجاح!")
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        bot.edit_message_text(f"❌ عذراً، تيك توك يرفض الطلب حالياً. حاول مع رابط آخر.", message.chat.id, msg.message_id)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
 
