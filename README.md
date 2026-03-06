import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# 1. السيرفر الوهمي
app = Flask('')
@app.route('/')
def home(): return "Exam Bot is Active!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run).start()

# 2. إعدادات البوت
API_TOKEN = '8629591404:AAElD9enpGE52EH8DNaNVeLJp14cU9eD64o'
bot = telebot.TeleBot(API_TOKEN)

# رابط صورة ترحيبية للبوت
START_IMAGE = 'https://telegra.ph/file/your-exam-image.jpg' 

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # إضافة المواد كأزرار
    btn1 = types.InlineKeyboardButton("📐 الرياضيات", callback_data="subject_math")
    btn2 = types.InlineKeyboardButton("📖 اللغة العربية", callback_data="subject_arabic")
    btn3 = types.InlineKeyboardButton("🧪 الفيزياء", callback_data="subject_physics")
    btn4 = types.InlineKeyboardButton("🧬 الأحياء", callback_data="subject_biology")
    
    markup.add(btn1, btn2, btn3, btn4)
    
    welcome_text = (
        f"📚 مرحباً بك يا {message.from_user.first_name} في بوت الامتحانات.\n\n"
        "هذا البوت مخصص لمساعدتك في الحصول على امتحانات الشهادة السابقة.\n\n"
        "👇 اختر المادة لبدء التصفح:"
    )
    bot.send_photo(message.chat.id, START_IMAGE, caption=welcome_text, reply_markup=markup)

# معالجة الضغط على الأزرار (المواد والسنوات)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # إذا اختار المستخدم مادة (مثلاً الرياضيات)
    if call.data == "subject_math":
        markup = types.InlineKeyboardMarkup(row_width=3)
        btn2020 = types.InlineKeyboardButton("2020", callback_data="file_math_2020")
        btn2021 = types.InlineKeyboardButton("2021", callback_data="file_math_2021")
        btn_back = types.InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")
        markup.add(btn2020, btn2021, btn_back)
        
        bot.edit_message_caption("📅 اختر سنة الامتحان (مادة الرياضيات):", 
                                 call.message.chat.id, call.message.message_id, reply_markup=markup)

    # إذا اختار سنة معينة (هنا نرسل الرابط أو الملف)
    elif call.data == "file_math_2020":
        bot.send_message(call.message.chat.id, "📄 جاري جلب امتحان الرياضيات 2020...")
        # هنا تضع رابط ملف الـ PDF الحقيقي
        pdf_url = "https://example.com/math_2020.pdf" 
        bot.send_document(call.message.chat.id, pdf_url, caption="✅ امتحان الرياضيات - عام 2020")

    elif call.data == "main_menu":
        start(call.message)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

