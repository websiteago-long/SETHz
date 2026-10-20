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

# Database ក្លែងក្លាយសម្រាប់ផ្ទុកទិន្នន័យអ្នកប្រើប្រាស់ (ប្រើ Dictionary)
users_db = {}

def track_user(user):
    """មុខងារសម្រាប់កត់ត្រាទុកអ្នកប្រើប្រាស់ថ្មីៗ និងអាប់ដេតទិន្នន័យ"""
    if user.id not in users_db:
        users_db[user.id] = {
            'first_name': user.first_name or "អតិថិជន",
            'username': user.username or "None",
            'balance': 0.00 # លុយចាប់ផ្តើមដំបូង
        }

# កំណត់តម្លៃ Robux សម្រាប់គណនា
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
        'btn_robux': "🎮 ទិញ Robux",
        'btn_back': "🔙 ត្រឡប់ក្រោយ",
        
        'deposit_text': "សូមជ្រើសរើសចំនួនទឹកប្រាក់ដែលអ្នកចង់ដាក់៖",
        'btn_custom_amount': "✍️ បំពេញចំនួនខ្លួនឯង",
        'custom_amount_prompt': "👇 សូមបញ្ជូលចំនួនទឹកប្រាក់ដែលអ្នកចង់ដាក់ (ឧទាហរណ៍: 1.50)៖\n\n🚫 វាយ /cancel ដើម្បីបោះបង់។",
        'generating_khqr': "⏳ សូមរង់ចាំ! កំពុងបង្កើត KHQR ចំនួន {amount} ដើម្បីទូទាត់...",
        'khqr_ready': "✅ នេះគឺជា KHQR របស់អ្នក សម្រាប់ចំនួន {amount}។\n\n⚠️ QR នេះនឹងលុបខ្លួនឯងដោយស្វ័យប្រវត្តិក្នុងរយៈពេល ៣ នាទី។\n\n👇 បន្ទាប់ពីទូទាត់រួច សូមផ្ញើវិក្កយបត្រ (Screenshot) មកកាន់ទីនេះ។\n\n🚫 វាយ /cancel ដើម្បីបោះបង់។",
        'receipt_received': "✅ ទទួលបានវិក្កយបត្រជោគជ័យ! សូមរង់ចាំ Admin ពិនិត្យនិងអនុម័តជូនអ្នក។",
        'cancelled': "🚫 ប្រតិបត្តិការត្រូវបានបោះបង់។ ត្រឡប់មកម៉ឺនុយដើម៖",
        
        'robux_text': "តារាងតម្លៃសម្រាប់ទិញ Robux :",
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
        'btn_robux': "🎮 Buy Robux",
        'btn_back': "🔙 Back",
        'deposit_text': "Please select the amount you want to deposit:",
        'btn_custom_amount': "✍️ Custom Amount",
        'custom_amount_prompt': "👇 Please enter the amount to deposit (e.g., 1.50):\n\n🚫 Type /cancel to abort.",
        'generating_khqr': "⏳ Please wait! Generating KHQR for {amount}...",
        'khqr_ready': "✅ Here is your KHQR for {amount}.\n\n⚠️ This QR will auto-delete in 3 minutes.\n\n👇 After paying, please send the receipt (Screenshot) here.\n\n🚫 Type /cancel to abort.",
        'receipt_received': "✅ Receipt received successfully! Please wait for Admin confirmation.",
        'cancelled': "🚫 Operation cancelled. Back to Main Menu:",
        'robux_text': "Pricing table for Robux :",
        'robux_selected': "You have selected the {package} package.\n\n👇 Please enter your Roblox Username below:\n\n🚫 Type /cancel to abort.",
        'username_received_insufficient': "✅ Received Username: {username} successfully!\n\nYou do not have enough balance to buy, please deposit 🤍🙏🏻",
        'username_received_success': "✅ Received Username: {username} successfully!\n\n✅ Balance deducted! Order successful, please wait for the code.",
        'main_menu_text': "You are back to the Main Menu:",
        'lang_changed': "Language changed to English 🇬🇧"
    }
}

def get_user_lang(chat_id):
    return user_languages.get(chat_id, 'kh')

def get_main_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton(texts[lang]['btn_manage']), KeyboardButton(texts[lang]['btn_rent']))
    markup.add(KeyboardButton(texts[lang]['btn_deposit']), KeyboardButton(texts[lang]['btn_change_lang'])) 
    return markup

def get_rent_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(texts[lang]['btn_robux']), KeyboardButton(texts[lang]['btn_back']))
    return markup

def get_deposit_keyboard(lang):
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton("$1.00", callback_data='dep_1.00'),
        InlineKeyboardButton("$2.00", callback_data='dep_2.00'),
        InlineKeyboardButton("$3.00", callback_data='dep_3.00'),
        InlineKeyboardButton("$4.00", callback_data='dep_4.00'),
        InlineKeyboardButton("$5.00", callback_data='dep_5.00')
    )
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

def delete_message_timer(chat_id, message_id):
    try: bot.delete_message(chat_id, message_id)
    except: pass 

@bot.message_handler(commands=['start'])
def send_welcome(message):
    track_user(message.from_user)
    chat_id = message.chat.id
    lang = get_user_lang(chat_id)
    image_url = "https://img.sanishtech.com/u/23589ed30a9f482112e591c0f4c9fa18.png"
    bot.send_photo(chat_id, photo=image_url, caption=texts[lang]['welcome'].format(name=message.from_user.first_name), reply_markup=get_main_keyboard(lang))

# ================= ផ្នែក ADMIN PANEL (/admin) =================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id != ADMIN_GROUP_ID and message.chat.id > 0:
        bot.reply_to(message, "❌ មុខងារនេះប្រើបានតែក្នុង Admin Group ប៉ុណ្ណោះ។")
        return

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📣 សារទៅអ្នកប្រើប្រាស់ទាំងអស់", callback_data="adm_sys_broadcast"),
        InlineKeyboardButton("👥 ឆែកមើលអ្នកប្រើប្រាស់ទាំងអស់", callback_data="adm_sys_users")
    )
    bot.reply_to(message, "🛠 <b>មឺនុយគ្រប់គ្រង (Admin Panel)</b>", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('adm_sys_'))
def handle_admin_system(call):
    action = call.data.split('_')[-1]
    bot.answer_callback_query(call.id)
    
    if action == 'users':
        if not users_db:
            bot.send_message(call.message.chat.id, "📭 មិនទាន់មានអ្នកប្រើប្រាស់នៅឡើយទេ។")
            return
            
        text = "👥 <b>បញ្ជីអ្នកប្រើប្រាស់ទាំងអស់:</b>\n\n"
        for uid, data in users_db.items():
            text += f"🆔 <code>{uid}</code>\n👤 {data['first_name']} (@{data['username']})\n💰 Balance: <b>${data['balance']:.2f}</b>\n〰️〰️〰️〰️〰️〰️〰️〰️\n"
        
        for i in range(0, len(text), 4000):
            bot.send_message(call.message.chat.id, text[i:i+4000], parse_mode="HTML")
            
    elif action == 'broadcast':
        msg = bot.send_message(call.message.chat.id, "✍️ <b>សូមវាយសារដែលអ្នកចង់ Broadcast:</b>\n\n<i>(វាយ /cancel ដើម្បីបោះបង់)</i>", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "🚫 បោះបង់ការផ្ញើសារ Broadcast។")
        return
        
    success = 0
    bot.send_message(message.chat.id, "⏳ កំពុងធ្វើការផ្ញើ...")
    for uid in users_db.keys():
        try:
            bot.send_message(uid, f"📣 <b>សារជូនដំណឹងពី Admin:</b>\n\n{message.text}", parse_mode="HTML")
            success += 1
        except: pass
            
    bot.send_message(message.chat.id, f"✅ ការ Broadcast ទទួលបានជោគជ័យ!\n👥 បានផ្ញើទៅកាន់: <b>{success} នាក់</b>", parse_mode="HTML")


# ================= ផ្នែក ដាក់ប្រាក់ (DEPOSIT) =================
@bot.callback_query_handler(func=lambda call: call.data.startswith('dep_'))
def handle_deposit_selection(call):
    chat_id = call.message.chat.id
    lang = get_user_lang(chat_id)
    bot.answer_callback_query(call.id)
    
    if call.data == 'dep_custom':
        msg = bot.send_message(chat_id, texts[lang]['custom_amount_prompt'])
        bot.register_next_step_handler(msg, process_custom_amount)
    else:
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
    loading_msg = bot.send_message(chat_id, texts[lang]['generating_khqr'].format(amount=amount))
    time.sleep(3)
    try: bot.delete_message(chat_id, loading_msg.message_id)
    except: pass
        
    khqr_url = "https://img.sanishtech.com/u/95f7764f8f7a67e3fd51da9a0ca17aac.jpeg"
    khqr_msg = bot.send_photo(chat_id, photo=khqr_url, caption=texts[lang]['khqr_ready'].format(amount=amount))
    
    threading.Timer(180.0, delete_message_timer, args=(chat_id, khqr_msg.message_id)).start()
    bot.register_next_step_handler(khqr_msg, lambda m: process_receipt(m, amount))

def process_receipt(message, amount):
    chat_id = message.chat.id
    lang = get_user_lang(chat_id)
    
    if message.text == '/cancel':
        bot.send_message(chat_id, texts[lang]['cancelled'], reply_markup=get_main_keyboard(lang))
        return
        
    bot.reply_to(message, texts[lang]['receipt_received'])
    
    amount_val = amount.replace('$', '')
    admin_markup = InlineKeyboardMarkup()
    admin_markup.add(
        InlineKeyboardButton("✅ Approve", callback_data=f"adm_app_dep_{chat_id}_{amount_val}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"adm_rej_dep_{chat_id}")
    )
    admin_markup.add(InlineKeyboardButton("💬 Reply ទៅកាន់ User", callback_data=f"adm_rep_{chat_id}"))
    
    caption_text = f"💰 <b>សំណើដាក់ប្រាក់ថ្មី</b>\n\n👤 ឈ្មោះ: {message.from_user.first_name}\n🆔 ID: <code>{chat_id}</code>\n💵 ចំនួន: <b>{amount}</b>"
    
    if message.content_type == 'photo':
        bot.send_photo(ADMIN_GROUP_ID, message.photo[-1].file_id, caption=caption_text, parse_mode="HTML", reply_markup=admin_markup)
    else:
        caption_text += "\n\n⚠️ <i>User មិនបានផ្ញើរូបភាពវិក្កយបត្រមកទេ!</i>"
        bot.send_message(ADMIN_GROUP_ID, caption_text, parse_mode="HTML", reply_markup=admin_markup)


# ================= ផ្នែក ROBUX =================
@bot.callback_query_handler(func=lambda call: call.data.startswith('robux_'))
def handle_robux_payment_callback(call):
    chat_id = call.message.chat.id
    lang = get_user_lang(chat_id)
    bot.answer_callback_query(call.id)
    
    selected_pkg_name = robux_names.get(call.data, "")
    msg = bot.send_message(chat_id, texts[lang]['robux_selected'].format(package=selected_pkg_name))
    
    bot.register_next_step_handler(msg, lambda m: process_robux_username(m, call.data))

def process_robux_username(message, package_key):
    chat_id = message.chat.id
    user_id = message.from_user.id
    track_user(message.from_user)
    lang = get_user_lang(chat_id)
    
    if message.text == '/cancel':
        bot.send_message(chat_id, texts[lang]['cancelled'], reply_markup=get_main_keyboard(lang))
        return
        
    username = message.text
    price = robux_prices.get(package_key, 0)
    package_name = robux_names.get(package_key, "Unknown")
    
    if users_db[user_id]['balance'] >= price:
        users_db[user_id]['balance'] -= price
        
        bot.reply_to(message, texts[lang]['username_received_success'].format(username=username))
        
        admin_markup = InlineKeyboardMarkup()
        admin_markup.add(
            InlineKeyboardButton("✅ បានផ្ញើកូដរួចរាល់", callback_data=f"adm_don_ord_{chat_id}"),
            InlineKeyboardButton("💬 Reply ទាក់ទងទៅ User", callback_data=f"adm_rep_{chat_id}")
        )
        order_text = f"🎮 <b>ការបញ្ជាទិញ Robux ថ្មី (បានកាត់លុយរួច)</b>\n\n👤 ឈ្មោះ: {message.from_user.first_name}\n🆔 ID: <code>{chat_id}</code>\n📦 កញ្ចប់: <b>{package_name}</b>\n🎮 Username: <code>{username}</code>\n\n✅ <i>ទឹកប្រាក់ ${price:.2f} ត្រូវបានកាត់ចេញពីគណនីអតិថិជនរួចរាល់។ សូម Admin ផ្ញើកូដអោយគាត់។</i>"
        bot.send_message(ADMIN_GROUP_ID, order_text, parse_mode="HTML", reply_markup=admin_markup)
        
    else:
        bot.reply_to(message, texts[lang]['username_received_insufficient'].format(username=username))


# ================= គ្រប់គ្រងសកម្មភាព ADMIN (APPROVE / REJECT) =================
@bot.callback_query_handler(func=lambda call: call.data.startswith('adm_'))
def handle_admin_actions(call):
    data_parts = call.data.split('_')
    action = data_parts[1] 
    
    if action == 'sys': return 
    
    type_ = data_parts[2] 
    user_id = int(data_parts[3]) 
    bot.answer_callback_query(call.id)
    
    if action == 'app' and type_ == 'dep':
        amount_val = float(data_parts[4])
        
        # Add balance to user
        if user_id in users_db:
            users_db[user_id]['balance'] += amount_val 
        else:
            # Just in case user is not in DB yet
            users_db[user_id] = {'first_name': "អតិថិជន", 'username': "None", 'balance': amount_val}
            
        bot.send_message(user_id, f"✅ សំណើដាក់ប្រាក់ចំនួន **${amount_val:.2f}** ត្រូវបានអនុម័តដោយ Admin ជោគជ័យ!\n\nទឹកប្រាក់ត្រូវបានបញ្ចូលទៅក្នុងគណនីរបស់អ្នក។", parse_mode="Markdown")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, f"✅ អនុម័តទឹកប្រាក់ **${amount_val:.2f}** ចូលគណនី (ID: {user_id}) រួចរាល់។", parse_mode="Markdown")
        
    elif action == 'rej' and type_ == 'dep':
        bot.send_message(user_id, "❌ សំណើដាក់ប្រាក់របស់អ្នកត្រូវបាន **បដិសេធ** ដោយ Admin!", parse_mode="Markdown")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, f"❌ បដិសេធវិក្កយបត្រ (ID: {user_id}) រួចរាល់។")
        
    elif action == 'don' and type_ == 'ord':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, f"✅ ដោះស្រាយការបញ្ជាទិញរបស់ ID: {user_id} រួចរាល់។")

    elif action == 'rep':
        msg = bot.send_message(call.message.chat.id, f"✍️ សូមវាយសារដែលអ្នកចង់ផ្ញើទៅកាន់ User (ID: {user_id}):\n*(វាយពាក្យ /cancel ដើម្បីបោះបង់)*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, lambda m: forward_to_user(m, user_id))

def forward_to_user(message, user_id):
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "🚫 បោះបង់ការផ្ញើសារ។")
        return
    bot.send_message(user_id, f"📩 <b>សារពី Admin:</b>\n\n{message.text}", parse_mode="HTML")
    bot.send_message(message.chat.id, f"✅ សារបានផ្ញើទៅកាន់ User ({user_id}) ជោគជ័យ!")


# ================= MAIN MENU & TEXT HANDLER =================
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    track_user(message.from_user)
    chat_id = message.chat.id
    user_name = message.from_user.first_name or "អតិថិជន"
    lang = get_user_lang(chat_id)
    text = message.text

    if text in [texts['kh']['btn_change_lang'], texts['en']['btn_change_lang']]:
        new_lang = 'en' if lang == 'kh' else 'kh'
        user_languages[chat_id] = new_lang
        bot.send_message(chat_id, texts[new_lang]['lang_changed'], reply_markup=get_main_keyboard(new_lang))

    elif text in [texts['kh']['btn_deposit'], texts['en']['btn_deposit']]:
        bot.send_message(chat_id, texts[lang]['deposit_text'], reply_markup=get_deposit_keyboard(lang))

    elif text in [texts['kh']['btn_manage'], texts['en']['btn_manage']]:
        current_balance = users_db.get(chat_id, {}).get('balance', 0.00)
        formatted_info = texts[lang]['account_info'].format(name=user_name, id=chat_id, balance=current_balance)
        bot.reply_to(message, formatted_info, parse_mode="HTML")

    elif text in [texts['kh']['btn_rent'], texts['en']['btn_rent']]:
        bot.send_message(chat_id, texts[lang]['rent_menu_text'], reply_markup=get_rent_keyboard(lang))

    elif text in [texts['kh']['btn_robux'], texts['en']['btn_robux']]:
        bot.send_message(chat_id, texts[lang]['robux_text'], reply_markup=get_robux_pricing_keyboard())

    elif text in [texts['kh']['btn_back'], texts['en']['btn_back']]:
        bot.send_message(chat_id, texts[lang]['main_menu_text'], reply_markup=get_main_keyboard(lang))

print("Bot កំពុងដំណើរការ...")
bot.polling(none_stop=True)
