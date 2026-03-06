import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# 1. إعداد السيرفر الوهمي لإبقاء البوت متصلاً على Render
app = Flask('')

@app.route('/')
def home():
    return "Exam Bot is Running!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. إعدادات البوت (التوكن الخاص بك)
API_TOKEN = '8629591404:AAElD9enpGE52EH8DNaNVeLJp14cU9eD64o'
bot = telebot.TeleBot(API_TOKEN)

# رابط صورة ترحيبية (يمكنك تغيير الرابط لاحقاً بصورتك الخاصة)
START_IMAGE = 'https://p7.itc.cn/images01/20210607/40608511746648e49d0738d8f0f08960.jpeg'

@bot.message_handler(commands=['start'])
def start(message):
    # إنشاء أزرار المواد
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("📐 الرياضيات", callback_data="math")
    btn2 = types.InlineKeyboardButton("📖 اللغة العربية", callback_data="arabic")
    btn3 = types.InlineKeyboardButton("🧪 الفيزياء", callback_data="physics")
    btn4 = types.InlineKeyboardButton("🧬 الأحياء", callback_data="biology")
    btn5 = types.InlineKeyboardButton("📜 التاريخ", callback_data="history")
    btn6 = types.InlineKeyboardButton("🕋 التربية الإسلامية", callback_data="islamic")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    welcome_text = (
        f"📚 مرحباً بك يا {message.from_user.first_name} في بوت امتحانات الشهادة.\n\n"
        "هذا البوت يساعدك في الوصول للامتحانات السابقة بسهولة.\n\n"
        "👇 اختر المادة التي تريدها:"
    )
    bot.send_photo(message.chat.id, START_IMAGE, caption=welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # عند اختيار مادة الرياضيات كمثال
    if call.data == "math":
        markup = types.InlineKeyboardMarkup(row_width=2)
        year2020 = types.InlineKeyboardButton("امتحان 2020", callback_data="math_2020")
        year2021 = types.InlineKeyboardButton("امتحان 2021", callback_data="math_2021")
        back = types.InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")
        markup.add(year2020, year2021, back)
        
        bot.edit_message_caption("📅 اختر سنة الامتحان لمادة الرياضيات:", 
                                 call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "main_menu":
        # العودة للقائمة الرئيسية
        start(call.message)
        bot.delete_message(call.message.chat.id, call.message.message_id)

    # مثال لإرسال ملف (ستحتاج لوضع الروابط الحقيقية هنا)
    elif call.data == "math_2020":
        bot.send_message(call.message.chat.id, "⏳ جاري جلب ملف امتحان الرياضيات 2020...")
        # يمكنك استبدال الرابط أدناه برابط ملف PDF حقيقي
        pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        bot.send_document(call.message.chat.id, pdf_url, caption="✅ امتحان الرياضيات 2020")

# 3. تشغيل البوت
if __name__ == "__main__":
    keep_alive()
    print("🚀 البوت يعمل الآن...")
    bot.infinity_polling()
