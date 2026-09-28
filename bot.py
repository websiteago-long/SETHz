import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ទាញយក Token ពី Railway Variables 
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# បង្កើតមុខងារសម្រាប់ហៅ Menu ដើមមកវិញ
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("🛒 TOUP SERVICE"), KeyboardButton("👨🏻‍💻ACCOUNT"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "សួស្តី! សូមជ្រើសរើសសេវាកម្មខាងក្រោម៖", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # ពេលចុច 🛒 TOUP SERVICE
    if message.text == "🛒 TOUP SERVICE":
        # បង្កើត Button ហ្គេមថ្មី
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(KeyboardButton("MOBILE"), KeyboardButton("ROBLOX"))
        markup.add(KeyboardButton("PUBG"), KeyboardButton("🔙 BACK"))
        bot.reply_to(message, "សូមជ្រើសរើសហ្គេមខាងក្រោម៖", reply_markup=markup)
        
    # ពេលចុចលើហ្គេមណាមួយ
    elif message.text in ["MOBILE", "ROBLOX", "PUBG"]:
        bot.reply_to(message, "ប្រព័ន្ធកំពុងជុសជុល…🙏🏻")
        
    # ពេលចុច 🔙 BACK ត្រឡប់មកដើមវិញ
    elif message.text == "🔙 BACK":
        bot.reply_to(message, "ត្រឡប់មកកាន់ Menu ដើមវិញ៖", reply_markup=main_menu())
        
    # ពេលចុច 👨🏻‍💻ACCOUNT
    elif message.text == "👨🏻‍💻ACCOUNT":
        bot.reply_to(message, "អ្នកបានជ្រើសរើស 👨🏻‍💻ACCOUNT!")
        
    else:
        bot.reply_to(message, "សូមជ្រើសរើសជម្រើសណាមួយពី Menu ខាងក្រោម។")

print("Bot is running...")
bot.infinity_polling()
