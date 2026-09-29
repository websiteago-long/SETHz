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
    markup.add(KeyboardButton("🎉 អ្នកលក់បន្ដរ"), KeyboardButton("📨Admin/Support")) 
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "សួស្តី! សូមជ្រើសរើសសេវាកម្មខាងក្រោម៖", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # ពេលចុច 🛒 TOUP SERVICE
    if message.text == "🛒 TOUP SERVICE":
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
        
    # ពេលចុច 📨Admin/Support
    elif message.text == "📨Admin/Support":
        bot.reply_to(message, "មានបញ្ហា ឬសំណួរអ្វី សូមទំនាក់ទំនងមកកាន់ Admin៖ @SETHSPp")
        
    # ពេលចុច 🎉 អ្នកលក់បន្ដរ
    elif message.text == "🎉 អ្នកលក់បន្ដរ":
        # បង្កើតប៊ូតុង BACK មួយទុកឲ្យគេចុចថយក្រោយ បើគេអត់មានកូដ
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(KeyboardButton("🔙 BACK"))
        
        msg = bot.reply_to(message, "សូមបញ្ចូលលេខកូដសម្ងាត់ ដើម្បីអាចក្លាយជាអ្នកលក់បន្ត៖", reply_markup=markup)
        # បញ្ជូនសារដែលគេវាយបន្ទាប់ ទៅកាន់មុខងារ check_passcode
        bot.register_next_step_handler(msg, check_passcode)
        
    else:
        bot.reply_to(message, "សូមជ្រើសរើសជម្រើសណាមួយពី Menu ខាងក្រោម។")

# មុខងារសម្រាប់ត្រួតពិនិត្យលេខកូដអ្នកលក់បន្ត
def check_passcode(message):
    if message.text == "🔙 BACK":
        bot.reply_to(message, "ត្រឡប់មកកាន់ Menu ដើមវិញ៖", reply_markup=main_menu())
    elif message.text == "SETHz12@@":
        bot.reply_to(message, "✅ លេខកូដត្រឹមត្រូវ! ឥឡូវនេះអ្នកគឺជាអ្នកលក់បន្ត។\n(ប្រព័ន្ធមុខងារលក់បន្តកំពុងរៀបចំ...)", reply_markup=main_menu())
    else:
        msg = bot.reply_to(message, "❌ លេខកូដមិនត្រឹមត្រូវទេ!\nសូមបញ្ចូលលេខកូដម្តងទៀត ឬចុច 🔙 BACK ដើម្បីត្រឡប់ក្រោយ៖")
        # បើវាយខុស អនុញ្ញាតឲ្យគេវាយម្តងទៀត
        bot.register_next_step_handler(msg, check_passcode)

print("Bot is running...")
bot.infinity_polling()
