import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os
import time
import threading

# យក Token ពី Environment Variables
TOKEN = os.environ.get('BOT_TOKEN', 'ដាក់_TOKEN_របស់អ្នកនៅទីនេះ')
bot = telebot.TeleBot(TOKEN)

# ID របស់ Admin Group 
ADMIN_GROUP_ID = -1003968009107 

user_languages = {}

# Database ក្លែងក្លាយសម្រាប់ផ្ទុកទិន្នន័យអ្នកប្រើប្រាស់
users_db = {}

def track_user(user):
    if user.id not in users_db:
        users_db[user.id] = {
            'first_name': user.first_name or "អតិថិជន",
            'username': user.username or "None",
            'balance': 0.00 
        }

robux_prices = {
    'robux_279': 3.10,
    'robux_362': 4.10,
    'robux_557': 6.10,
    'robux_1000': 9.99
}

robux_names = {
    'robux_279': "279 Robux ($3.10)",
    'robux_362': "362 Robux ($4.10)",
    'robux_557': "557 Robux ($6.10)",
    'robux_1000': "1000 Robux ($9.99)"
}

texts = {
    'kh': {
        'welcome': "សួស្តី {name}! សូមជ្រើសរើសសេវាកម្មខាងក្រោម៖",
        'select_below': "👇 សូមជ្រើសរើសជម្រើសនៅខាងក្រោម៖",
        'btn_manage': "👨🏻‍💻 គ្រប់គ្រងគណនី",
        'btn_rent': "🛍 ហាងសេវា", 
        'btn_deposit': "💰 ដាក់ប្រាក់", 
        'btn_change_lang': "🌐 ភាសា", 
        'account_info': "👨🏻‍💻ព័ត៌មានគណនី \n🌸➖➖➖➖🌸➖➖➖🌸\n  👨🏻‍💻 Name : {name}\n  🆔 ID : <code>{id}</code>\n🌸\n  💼 Balance : <b>${balance:.2f}</b>\n  🌟 Rank : Member\n🌸➖➖➖➖🌸➖➖➖🌸",
        'rent_menu_text': "សូមជ្រើសរើសសេវាកម្មដែលអ្នកចង់បានខាងក្រោម៖",
        'btn_robux': "🎮 Roblox Code", # បានប្តូរឈ្មោះនៅទីនេះ
        'btn_back': "🔙 ត្រឡប់ក្រោយ",
        'deposit_text': "សូមជ្រើសរើសចំនួនទឹកប្រាក់ដែលអ្នកចង់ដាក់៖",
        'btn_custom_amount': "✍️ បំពេញចំនួនខ្លួនឯង",
        'custom_amount_prompt': "👇 សូមបញ្ជូលចំនួនទឹកប្រាក់ដែលអ្នកចង់ដាក់ (ឧទាហរណ៍: 1.50)៖\n\n🚫 វាយ /cancel ដើម្បីបោះបង់។",
        'generating_khqr': "⏳ សូមរង់ចាំ! កំពុងបង្កើត KHQR ចំនួន {amount} ដើម្បីទូទាត់...",
        'khqr_ready': "✅ នេះគឺជា KHQR របស់អ្នក សម្រាប់ចំនួន {amount}។\n\n⚠️ QR នេះនឹងលុបខ្លួនឯងដោយស្វ័យប្រវត្តិក្នុងរយៈពេល ៣ នាទី។\n\n👇 បន្ទាប់ពីទូទាត់រួច សូមផ្ញើវិក្កយបត្រ (Screenshot) មកកាន់ទីនេះ។\n\n🚫 វាយ /cancel ដើម្បីបោះបង់។",
        'receipt_received': "✅ ទទួលបានវិក្កយបត្រជោគជ័យ! សូមរង់ចាំ Admin ពិនិត្យនិងអនុម័តជូនអ្នក។",
        'cancelled': "🚫 ប្រតិបត្តិការត្រូវបានបោះបង់។ ត្រឡប់មកម៉ឺនុយដើម៖",
        'robux_text': "តារាងតម្លៃសម្រាប់ទិញ Roblox Code :",
        'robux_selected': "អ្នកបានជ្រើសរើសទិញកញ្ចប់ {package} ។\n\n👇 សូមបញ្ជូល Username Roblox របស់អ្នកខាងក្រោម៖\n\n🚫 វាយ /cancel ដើម្បីបោះបង់។",
        'username_received_insufficient': "✅ ទទួលបាន Username: {username} ជោគជ័យ!\n\nអ្នកមិនមានលុយគ្រប់គ្រាន់ដើម្បីទិញទេ សូមធ្វើការដាក់ប្រាក់ 🤍🙏🏻",
        'username_received_success': "✅ ទទួលបាន Username: {username} ជោគជ័យ!\n\n✅ ទឹកប្រាក់ត្រូវបានកាត់ចេញពីគណនី! បញ្ជាទិញជោគជ័យ សូមរង់ចាំទទួលកូដ។",
        'main_menu_text': "អ្នកបានត្រឡប់មកម៉ឺនុយដើមវិញ៖",
        'lang_changed': "ភាសាត្រូវបានផ្លាស់ប្តូរទៅជា ខ្មែរ 🇰🇭"
    },
    'en': {
        'welcome': "Hello {name}! Please select a service below:",
        'select_below': "👇 Please select an option below:",
        'btn_manage': "👨🏻‍💻 Manage Account",
        'btn_rent': "🛍 Service Shop", 
        'btn_deposit': "💰 Deposit", 
        'btn_change_lang': "🌐 ភាសា", 
        'account_info': "👨🏻‍💻Account Info \n🌸➖➖➖➖🌸➖➖➖🌸\n  👨🏻‍💻 Name : {name}\n  🆔 ID : <code>{id}</code>\n🌸\n  💼 Balance : <b>${balance:.2f}</b>\n  🌟 Rank : Member\n🌸➖➖➖➖🌸➖➖➖🌸",
        'rent_menu_text': "Please select a service you want below:",
        'btn_robux': "🎮 Roblox Code", # បានប្តូរឈ្មោះនៅទីនេះ
        'btn_back': "🔙 Back",
        'deposit_text': "Please select the amount you want to deposit:",
        'btn_custom_amount': "✍️ Custom Amount",
        'custom_amount_prompt': "👇 Please enter the amount to deposit (e.g., 1.50):\n\n🚫 Type /cancel to abort.",
        'generating_khqr': "⏳ Please wait! Generating KHQR for {amount}...",
        'khqr_ready': "✅ Here is your KHQR for {amount}.\n\n⚠️ This QR will auto-delete in 3 minutes.\n\n👇 After paying, please send the receipt (Screenshot) here.\n\n🚫 Type /cancel to abort.",
        'receipt_received': "✅ Receipt received successfully! Please wait for Admin confirmation.",
        'cancelled': "🚫 Operation cancelled. Back to Main Menu:",
        'robux_text': "Pricing table for Roblox Code :",
        'robux_selected': "You have selected the {package} package.\n\n👇 Please enter your Roblox Username below:\n\n🚫 Type /cancel to abort.",
        'username_received_insufficient': "✅ Received Username: {username} successfully!\n\nYou do not have enough balance to buy, please deposit 🤍🙏🏻",
        'username_received_success': "✅ Received Username: {username} successfully!\n\n✅ Balance deducted! Order successful, please wait for the code.",
        'main_menu_text': "You are back to the Main Menu:",
        'lang_changed': "Language changed to English 🇬🇧"
    }
}

def get_user_lang(chat_id): return user_languages.get(chat_id, 'kh')

def get_main_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton(texts[lang]['btn_manage']), KeyboardButton(texts[lang]['btn_rent']))
    markup.add(KeyboardButton(texts[lang]['btn_deposit']), KeyboardButton(texts[lang]['btn_change_lang'])) 
    return markup

def get_rent_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton(texts[lang]['btn_robux']), KeyboardButton(texts[lang]['btn_back']))
    return markup

def get_deposit_keyboard(lang):
    markup = InlineKeyboardMarkup
