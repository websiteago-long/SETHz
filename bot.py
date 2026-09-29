import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ទាញយក Token ពី Railway Variables 
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# បង្កើតកន្លែងផ្ទុកទិន្នន័យបណ្តោះអាសន្នសម្រាប់អ្នកលក់បន្ត
resellers = set()

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
        # ទាញយកព័ត៌មានអ្នកប្រើប្រាស់
        user_id = message.from_user.id
        first_name = message.from_user.first_name or ""
        last_name = message.from_user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
        
        username = message.from_user.username
        username_display = f"@{username}" if username else "គ្មាន"
        
        # កំណត់ឋានៈ (Rank)
        if username and username.lower() == "longzzsmmdigitall":
            rank = "👑 VIP Admin"
        elif user_id in resellers:
            rank = "🌟 Legend អ្នកលក់បន្ដរ"
        else:
            rank = "🥉 noob អ្នកទិញធម្មតា"
            
        balance = 0.00 # លំនាំដើម $0.00
        
        # រៀបចំទម្រង់សារបង្ហាញ
        account_info = f"""
👤 **ព័ត៌មានគណនីរបស់អ្នក**
➖➖➖➖➖➖➖➖➖➖
🔹 **ឈ្មោះ (Name):** {full_name}
🔹 **Username:** {username_display}
🔹 **លេខសម្គាល់ (ID):** `{user_id}`
🔹 **ឋានៈ (Rank):** {rank}
🔹 **សមតុល្យ (Balance):** ${balance:.2f}
➖➖➖➖➖➖➖➖➖➖
"""
        bot.reply_to(message, account_info, parse_mode='Markdown')
        
    # ពេលចុច 📨Admin/Support
    elif message.text == "📨Admin/Support":
        bot.reply_to(message, "មានបញ្ហា ឬសំណួរអ្វី សូមទំនាក់ទំនងមកកាន់ Admin៖ @SETHSPp")
        
    # ពេលចុច 🎉 អ្នកលក់បន្ដរ
    elif message.text == "🎉 អ្នកលក់បន្ដរ":
        # បើគាត់ជា VIP ឬ Legend ស្រាប់ មិនបាច់ឲ្យវាយកូដទៀតទេ
        if (message.from_user.username and message.from_user.username.lower() == "longzzsmmdigitall") or (message.from_user.id in resellers):
            bot.reply_to(message, "✅ អ្នកមានឋានៈជាអ្នកលក់បន្ត (Legend/VIP) រួចហើយ!", reply_markup=main_menu())
            return

        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(KeyboardButton("🔙 BACK"))
        
        msg = bot.reply_to(message, "សូមបញ្ចូលលេខកូដសម្ងាត់ ដើម្បីអាចក្លាយជាអ្នកលក់បន្ត៖", reply_markup=markup)
        bot.register_next_step_handler(msg, check_passcode)
        
    else:
        bot.reply_to(message, "សូមជ្រើសរើសជម្រើសណាមួយពី Menu ខាងក្រោម។")

# មុខងារសម្រាប់ត្រួតពិនិត្យលេខកូដអ្នកលក់បន្ត
def check_passcode(message):
    if message.text == "🔙 BACK":
        bot.reply_to(message, "ត្រឡប់មកកាន់ Menu ដើមវិញ៖", reply_markup=main_menu())
    elif message.text == "SETHz12@@":
        resellers.add(message.from_user.id) # កត់ត្រា ID គាត់ទុកជាអ្នកលក់បន្ត
        bot.reply_to(message, "✅ លេខកូដត្រឹមត្រូវ! ឥឡូវនេះអ្នកគឺជាអ្នកលក់បន្ត (Legend)។\nសូមចូលទៅកាន់ 👨🏻‍💻ACCOUNT ដើម្បីមើលឋានៈរបស់អ្នក។", reply_markup=main_menu())
    else:
        msg = bot.reply_to(message, "❌ លេខកូដមិនត្រឹមត្រូវទេ!\nសូមបញ្ចូលលេខកូដម្តងទៀត ឬចុច 🔙 BACK ដើម្បីត្រឡប់ក្រោយ៖")
        bot.register_next_step_handler(msg, check_passcode)

print("Bot is running...")
bot.infinity_polling()
