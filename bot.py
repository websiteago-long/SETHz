import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os
import time
import threading

# យក Token ពី Environment Variables
TOKEN = os.environ.get('BOT_TOKEN', 'ដាក់_TOKEN_របស់អ្នកនៅទីនេះ')
bot = telebot.TeleBot(TOKEN)

user_languages = {}

texts = {
    'kh': {
        'welcome': "សួស្តី {name}! សូមជ្រើសរើសសេវាកម្មខាងក្រោម៖",
        'select_below': "👇 សូមជ្រើសរើសជម្រើសនៅខាងក្រោម៖",
        'btn_manage': "👨🏻‍💻 គ្រប់គ្រងគណនី",
        'btn_rent': "🛍 ហាងសេវា", 
        'btn_deposit': "💰 ដាក់ប្រាក់", # ប៊ូតុងថ្មី
        'btn_change_lang': "🇬🇧 ភាសាអង់គ្លេស (English)", 
        'manage_text': "នេះគឺជាទំព័រសម្រាប់ គ្រប់គ្រងគណនី របស់អ្នក។",
        'rent_menu_text': "សូមជ្រើសរើសសេវាកម្មដែលអ្នកចង់បានខាងក្រោម៖",
        'btn_robux': "🎮 ទិញ Robux",
        'btn_back': "🔙 ត្រឡប់ក្រោយ",
        
        # ផ្នែកដាក់ប្រាក់
        'deposit_text': "សូមជ្រើសរើសចំនួនទឹកប្រាក់ដែលអ្នកចង់ដាក់៖",
        'btn_custom_amount': "✍️ បំពេញចំនួនខ្លួនឯង",
        'custom_amount_prompt': "👇 សូមបញ្ជូលចំនួនទឹកប្រាក់ដែលអ្នកចង់ដាក់ (ឧទាហរណ៍: 1.50)៖\n\n🚫 វាយ /cancel ដើម្បីបោះបង់។",
        'generating_khqr': "⏳ សូមរង់ចាំ! កំពុងបង្កើត KHQR ចំនួន {amount} ដើម្បីទូទាត់...",
        'khqr_ready': "✅ នេះគឺជា KHQR របស់អ្នក សម្រាប់ចំនួន {amount}។\n\n⚠️ QR នេះនឹងលុបខ្លួនឯងដោយស្វ័យប្រវត្តិក្នុងរយៈពេល ៣ នាទី។\n\n👇 បន្ទាប់ពីទូទាត់រួច សូមផ្ញើវិក្កយបត្រ (Screenshot) មកកាន់ទីនេះ។\n\n🚫 វាយ /cancel ដើម្បីបោះបង់ការដាក់ប្រាក់។",
        'receipt_received': "✅ ទទួលបានវិក្កយបត្រជោគជ័យ! សូមរង់ចាំ Admin ពិនិត្យនិងបញ្ចូលប្រាក់ជូនអ្នក។",
        'cancelled': "🚫 ប្រតិបត្តិការត្រូវបានបោះបង់។ ត្រឡប់មកម៉ឺនុយដើម៖",
        
        # ផ្នែក Robux
        'robux_text': "តារាងតម្លៃសម្រាប់ទិញ Robux :",
        'robux_selected': "អ្នកបានជ្រើសរើសទិញកញ្ចប់ {package} ។\n\n👇 សូមបញ្ជូល Username Roblox របស់អ្នកខាងក្រោម៖\n\n🚫 វាយ /cancel ដើម្បីបោះបង់។",
        'username_received': "✅ ទទួលបាន Username: {username} ជោគជ័យ!\n\nសូមធ្វើការបង់ប្រាក់ រួចផ្ញើវិក្កយបត្រ (Screenshot) មកកាន់ទីនេះ។",
        
        'main_menu_text': "អ្នកបានត្រឡប់មកម៉ឺនុយដើមវិញ៖",
        'lang_changed': "ភាសាត្រូវបានផ្លាស់ប្តូរទៅជា ខ្មែរ 🇰🇭"
    },
    'en': {
        'welcome': "Hello {name}! Please select a service below:",
        'select_below': "👇 Please select an option below:",
        'btn_manage': "👨🏻‍💻 Manage Account",
        'btn_rent': "🛍 Service Shop", 
        'btn_deposit': "💰 Deposit", 
        'btn_change_lang': "🇰🇭 ភាសាខ្មែរ (Khmer)", 
        'manage_text': "This is your Account Management page.",
        'rent_menu_text': "Please select a service you want below:",
        'btn_robux': "🎮 Buy Robux",
        'btn_back': "🔙 Back",
        
        # Deposit Section
        'deposit_text': "Please select the amount you want to deposit:",
        'btn_custom_amount': "✍️ Custom Amount",
        'custom_amount_prompt': "👇 Please enter the amount to deposit (e.g., 1.50):\n\n🚫 Type /cancel to abort.",
        'generating_khqr': "⏳ Please wait! Generating KHQR for {amount}...",
        'khqr_ready': "✅ Here is your KHQR for {amount}.\n\n⚠️ This QR will auto-delete in 3 minutes.\n\n👇 After paying, please send the receipt (Screenshot) here.\n\n🚫 Type /cancel to abort the deposit.",
        'receipt_received': "✅ Receipt received successfully! Please wait for Admin confirmation.",
        'cancelled': "🚫 Operation cancelled. Back to Main Menu:",
        
        # Robux Section
        'robux_text': "Pricing table for Robux :",
        'robux_selected': "You have selected the {package} package.\n\n👇 Please enter your Roblox Username below:\n\n🚫 Type /cancel to abort.",
        'username_received': "✅ Received Username: {username} successfully!\n\nPlease make a payment and send the receipt (Screenshot) here.",
        
        'main_menu_text': "You are back to the Main Menu:",
        'lang_changed': "Language changed to English 🇬🇧"
    }
}

def get_user_lang(chat_id):
    return user_languages.get(chat_id, 'kh')

# ម៉ឺនុយដើម (បន្ថែមប៊ូតុង ដាក់ប្រាក់)
def get_main_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton(texts[lang]['btn_manage']), KeyboardButton(texts[lang]['btn_deposit']))
    markup.add(KeyboardButton(texts[lang]['btn_rent']), KeyboardButton(texts[lang]['btn_change_lang'])) 
    return markup

def get_rent_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(texts[lang]['btn_robux']))
    markup.add(KeyboardButton(texts[lang]['btn_back']))
    return markup

# កូនប៊ូតុងសម្រាប់ដាក់ប្រាក់ (Inline)
def get_deposit_keyboard(lang):
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton("$1.00", callback_data='dep_1.00'),
        InlineKeyboardButton("$2.00", callback_data='dep_2.00'),
        InlineKeyboardButton("$3.00", callback_data='dep_3.00'),
        InlineKeyboardButton("$4.00", callback_data='dep_4.00'),
        InlineKeyboardButton("$5.00", callback_data='dep_5.00')
    )
    # ដាក់ប៊ូតុងបំពេញខ្លួនឯងនៅខាងក្រោមគេ ១ជួរពេញ
    markup.row(InlineKeyboardButton(texts[lang]['btn_custom_amount'], callback_data='dep_custom'))
    return markup

def get_robux_pricing_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🪙 279 Robux - $3.10", callback_data='robux_279'),
        InlineKeyboardButton("🪙 362 Robux - $4.10", callback_data='robux_362'),
        InlineKeyboardButton("🪙 557 Robux - $6.10", callback_data='robux_557'),
        InlineKeyboardButton("🪙 1000 Robux - $9.99", callback_data='robux_1000')
    )
    return markup

# មុខងារសម្រាប់លុបសារ KHQR ក្រោយ ៣នាទី
def delete_message_timer(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        pass # បើអ្នកប្រើប្រាស់លុបមុន វានឹងរំលង Error នេះ

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name or "អតិថិជន"
    lang = get_user_lang(chat_id)
    image_url = "https://img.sanishtech.com/u/23589ed30a9f482112e591c0f4c9fa18.png"
    bot.send_photo(chat_id, photo=image_url, caption=texts[lang]['welcome'].format(name=user_name))
    bot.send_message(chat_id, texts[lang]['select_below'], reply_markup=get_main_keyboard(lang))

# ----------------- ផ្នែក ដាក់ប្រាក់ (DEPOSIT) -----------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('dep_'))
def handle_deposit_selection(call):
    chat_id = call.message.chat.id
    lang = get_user_lang(chat_id)
    bot.answer_callback_query(call.id)
    
    if call.data == 'dep_custom':
        msg = bot.send_message(chat_id, texts[lang]['custom_amount_prompt'])
        bot.register_next_step_handler(msg, process_custom_amount)
    else:
        # ទាញយកចំនួនលុយពី callback data (ឧ. dep_1.00 -> 1.00)
        amount = f"${call.data.split('_')[1]}"
        process_khqr_generation(chat_id, amount, lang)

def process_custom_amount(message):
    chat_id = message.chat.id
    lang = get_user_lang(chat_id)
    
    if message.text == '/cancel':
        bot.send_message(chat_id, texts[lang]['cancelled'], reply_markup=get_main_keyboard(lang))
        return
        
    amount = f"${message.text}"
    process_khqr_generation(chat_id, amount, lang)

def process_khqr_generation(chat_id, amount, lang):
    # ផ្ញើសារប្រាប់ថាកំពុងបង្កើត
    loading_msg = bot.send_message(chat_id, texts[lang]['generating_khqr'].format(amount=amount))
    
    # រង់ចាំ ៥ វិនាទី
    time.sleep(5)
    
    # លុបសារ "កំពុងបង្កើត..." ចេញវិញ
    try:
        bot.delete_message(chat_id, loading_msg.message_id)
    except:
        pass
        
    # ផ្ញើ KHQR ចូល
    khqr_url = "https://img.sanishtech.com/u/95f7764f8f7a67e3fd51da9a0ca17aac.jpeg"
    khqr_msg = bot.send_photo(chat_id, photo=khqr_url, caption=texts[lang]['khqr_ready'].format(amount=amount))
    
    # បញ្ជាឱ្យលុប KHQR នេះក្នុងរយៈពេល ៣ នាទី (180 វិនាទី) ដោយប្រើ Thread ដើម្បីកុំឱ្យគាំង Bot
    threading.Timer(180.0, delete_message_timer, args=(chat_id, khqr_msg.message_id)).start()
    
    # ចាំទទួលវិក្កយបត្រ (ឬពាក្យ /cancel)
    bot.register_next_step_handler(khqr_msg, process_receipt)

def process_receipt(message):
    chat_id = message.chat.id
    lang = get_user_lang(chat_id)
    
    if message.text == '/cancel':
        bot.send_message(chat_id, texts[lang]['cancelled'], reply_markup=get_main_keyboard(lang))
        return
        
    bot.reply_to(message, texts[lang]['receipt_received'])


# ----------------- ផ្នែក ROBUX -----------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('robux_'))
def handle_robux_payment_callback(call):
    chat_id = call.message.chat.id
    lang = get_user_lang(chat_id)
    bot.answer_callback_query(call.id)
    
    robux_packages = {
        'robux_279': "279 Robux ក្នុងតម្លៃ $3.10",
        'robux_362': "362 Robux ក្នុងតម្លៃ $4.10",
        'robux_557': "557 Robux ក្នុងតម្លៃ $6.10",
        'robux_1000': "1000 Robux ក្នុងតម្លៃ $9.99"
    }
    selected_package = robux_packages.get(call.data, "")
    msg = bot.send_message(chat_id, texts[lang]['robux_selected'].format(package=selected_package))
    bot.register_next_step_handler(msg, process_robux_username)

def process_robux_username(message):
    chat_id = message.chat.id
    lang = get_user_lang(chat_id)
    
    if message.text == '/cancel':
        bot.send_message(chat_id, texts[lang]['cancelled'], reply_markup=get_main_keyboard(lang))
        return
        
    username = message.text
    bot.reply_to(message, texts[lang]['username_received'].format(username=username))


# ----------------- គ្រប់គ្រងការចុចម៉ឺនុយទូទៅ -----------------
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    lang = get_user_lang(chat_id)
    text = message.text

    if text in [texts['kh']['btn_change_lang'], texts['en']['btn_change_lang']]:
        new_lang = 'en' if lang == 'kh' else 'kh'
        user_languages[chat_id] = new_lang
        bot.send_message(chat_id, texts[new_lang]['lang_changed'], reply_markup=get_main_keyboard(new_lang))

    elif text in [texts['kh']['btn_deposit'], texts['en']['btn_deposit']]:
        bot.send_message(chat_id, texts[lang]['deposit_text'], reply_markup=get_deposit_keyboard(lang))

    elif text in [texts['kh']['btn_manage'], texts['en']['btn_manage']]:
        bot.reply_to(message, texts[lang]['manage_text'])

    elif text in [texts['kh']['btn_rent'], texts['en']['btn_rent']]:
        bot.send_message(chat_id, texts[lang]['rent_menu_text'], reply_markup=get_rent_keyboard(lang))

    elif text in [texts['kh']['btn_robux'], texts['en']['btn_robux']]:
        bot.send_message(chat_id, texts[lang]['robux_text'], reply_markup=get_robux_pricing_keyboard())

    elif text in [texts['kh']['btn_back'], texts['en']['btn_back']]:
        bot.send_message(chat_id, texts[lang]['main_menu_text'], reply_markup=get_main_keyboard(lang))

print("Bot កំពុងដំណើរការ...")
bot.polling(none_stop=True)
