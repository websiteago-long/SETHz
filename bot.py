import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ទាញយក Token ពី Railway Variables 
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # បង្កើត Button នៅខាងក្រោមកន្លែងសរសេរអក្សរ
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton("🛒 TOUP SERVICE")
    btn2 = KeyboardButton("👨🏻‍💻ACCOUNT")
    
    # បញ្ចូល Button
    markup.add(btn1, btn2)

    bot.reply_to(message, "សួស្តី! សូមជ្រើសរើសសេវាកម្មខាងក្រោម៖", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "🛒 TOUP SERVICE":
        bot.reply_to(message, "អ្នកបានជ្រើសរើស 🛒 TOUP SERVICE!")
    elif message.text == "👨🏻‍💻ACCOUNT":
        bot.reply_to(message, "អ្នកបានជ្រើសរើស 👨🏻‍💻ACCOUNT!")
    else:
        bot.reply_to(message, "សូមជ្រើសរើសជម្រើសណាមួយពី Menu ខាងក្រោម។")

print("Bot is running...")
bot.infinity_polling()
