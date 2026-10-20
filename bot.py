import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os

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
        'btn_change_lang': "🇬🇧 ភាសាអង់គ្លេស (English)", 
        'manage_text': "នេះគឺជាទំព័រសម្រាប់ គ្រប់គ្រងគណនី របស់អ្នក។",
        'rent_menu_text': "សូមជ្រើសរើសសេវាកម្មដែលអ្នកចង់បានខាងក្រោម៖",
        'btn_robux': "🎮 ទិញ Robux",
        'btn_back': "🔙 ត្រឡប់ក្រោយ",
        
        # ផ្នែក Robux
        'robux_text': "តារាងតម្លៃសម្រាប់ទិញ Robux :",
        'robux_selected': "អ្នកបានជ្រើសរើសទិញកញ្ចប់ {package} ។\n\n👇 សូមបញ្ជូល Username Roblox របស់អ្នកខាងក្រោម៖",
        'username_received': "✅ ទទួលបាន Username: {username} ជោគជ័យ!\n\nសូមធ្វើការបង់ប្រាក់ រួចផ្ញើវិក្កយបត្រ (Screenshot) មកកាន់ទីនេះ។",
        
        'main_menu_text': "អ្នកបានត្រឡប់មកម៉ឺនុយដើមវិញ៖",
        'lang_changed': "ភាសាត្រូវបានផ្លាស់ប្តូរទៅជា ខ្មែរ 🇰🇭"
    },
    'en': {
        'welcome': "Hello {name}! Please select a service below:",
        'select_below': "👇 Please select an option below:",
        'btn_manage': "👨🏻‍💻 Manage Account",
        'btn_rent': "🛍 Service Shop", 
        'btn_change_lang': "🇰🇭 ភាសាខ្មែរ (Khmer)", 
        'manage_text': "This is your Account Management page.",
        'rent_menu_text': "Please select a service you want below:",
        'btn_robux': "🎮 Buy Robux",
        'btn_back': "🔙 Back",
        
        # Robux Section
        'robux_text': "Pricing table for Robux :",
        'robux_selected': "You have selected the {package} package.\n\n👇 Please enter your Roblox Username below:",
        'username_received': "✅ Received Username: {username} successfully!\n\nPlease make a payment and send the receipt (Screenshot) here.",
        
        'main_menu_text': "You are back to the Main Menu:",
        'lang_changed': "Language changed to English 🇬🇧"
    }
}

def get_user_lang(chat_id):
    return user_languages.get(chat_id, 'kh')

# ម៉ឺនុយដើម
def get_main_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton(texts[lang]['btn_manage']), KeyboardButton(texts[lang]['btn_rent']))
    markup.add(KeyboardButton(texts[lang]['btn_change_lang'])) 
    return markup

# ម៉ឺនុយហាងសេវា (នៅសល់តែ Robux)
def get_rent_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(texts[lang]['btn_robux']))
    markup.add(KeyboardButton(texts[lang]['btn_back']))
    return markup

# តារាងតម្លៃ Robux
def get_robux_pricing_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🪙 279 Robux - $3.10", callback_data='robux_279'),
        InlineKeyboardButton("🪙 362 Robux - $4.10", callback_data='robux_362'),
        InlineKeyboardButton("🪙 557 Robux - $6.10", callback_data='robux_557'),
        InlineKeyboardButton("🪙 1000 Robux - $9.99", callback_data='robux_1000')
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name or "អតិថិជន"
    lang = get_user_lang(chat_id)
    
    image_url = "https://img.sanishtech.com/u/23589ed30a9f482112e591c0f4c9fa18.png"
    
    bot.send_photo(chat_id, photo=image_url, caption=texts[lang]['welcome'].format(name=user_name))
    bot.send_message(chat_id, texts[lang]['select_below'], reply_markup=get_main_keyboard(lang))


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
