import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os
import time
import threading

TOKEN = os.environ.get('BOT_TOKEN', 'ដាក់_TOKEN_របស់អ្នកនៅទីនេះ')
bot = telebot.TeleBot(TOKEN)
ADMIN_GROUP_ID = -1003968009107 
ADMIN_USER_ID = 8904196183 

user_languages = {}
users_db = {}

robux_db = {
    'robux_1': {'name': '279 Robux', 'price': 3.10},
    'robux_2': {'name': '362 Robux', 'price': 4.10},
    'robux_3': {'name': '557 Robux', 'price': 6.10},
    'robux_4': {'name': '1000 Robux', 'price': 9.99}
}

admin_editing_robux = {}

def track_user(user):
    if user.id not in users_db:
        users_db[user.id] = {'first_name': user.first_name or "អតិថិជន", 'username': user.username or "None", 'balance': 0.00}

texts = {
    'kh': {
        'welcome': "សួស្តី {name}! សូមជ្រើសរើសសេវាកម្មខាងក្រោម៖",
        'select_below': "👇 សូមជ្រើសរើសជម្រើសនៅខាងក្រោម៖",
        'btn_manage': "👨🏻‍💻 គ្រប់គ្រងគណនី",
        'btn_rent': "🛍 ហាងសេវា", 'btn_deposit': "💰 ដាក់ប្រាក់", 'btn_change_lang': "🌐 ភាសា", 
        'account_info': "👨🏻‍💻ព័ត៌មានគណនី \n🌸➖➖➖➖🌸➖➖➖🌸\n  👨🏻‍💻 Name : {name}\n  🆔 ID : <code>{id}</code>\n🌸\n  💼 Balance : <b>${balance:.2f}</b>\n  🌟 Rank : Member\n🌸➖➖➖➖🌸➖➖➖🌸",
        'rent_menu_text': "សូមជ្រើសរើសសេវាកម្មដែលអ្នកចង់បានខាងក្រោម៖",
        'btn_robux': "🎮 Roblox Code", 'btn_back': "🔙 ត្រឡប់ក្រោយ",
        'deposit_text': "សូមជ្រើសរើសចំនួនទឹកប្រាក់ដែលអ្នកចង់ដាក់៖",
        'btn_custom_amount': "✍️ បំពេញចំនួនខ្លួនឯង",
        'custom_amount_prompt': "👇 សូមបញ្ជូលចំនួនទឹកប្រាក់ដែលអ្នកចង់ដាក់ (ឧទាហរណ៍: 1.50)៖\n\n🚫 វាយ /cancel ដើម្បីបោះបង់។",
        'generating_khqr': "⏳ សូមរង់ចាំ! កំពុងបង្កើត KHQR ចំនួន {amount} ដើម្បីទូទាត់...",
        'khqr_ready': "✅ នេះគឺជា KHQR របស់អ្នក សម្រាប់ចំនួន {amount}។\n\n⚠️ QR នេះនឹងលុបខ្លួនឯងដោយស្វ័យប្រវត្តិក្នុងរយៈពេល ៣ នាទី។\n\n👇 បន្ទាប់ពីទូទាត់រួច សូមផ្ញើវិក្កយបត្រមកទីនេះ។\n\n🚫 វាយ /cancel ដើម្បីបោះបង់។",
        'receipt_received': "✅ ទទួលបានវិក្កយបត្រជោគជ័យ! សូមរង់ចាំ Admin ពិនិត្យ។",
        'cancelled': "🚫 ប្រតិបត្តិការត្រូវបានបោះបង់។ ត្រឡប់មកម៉ឺនុយដើម៖",
        'robux_text': "តារាងតម្លៃសម្រាប់ទិញ Roblox Code :",
        'robux_selected': "អ្នកបានជ្រើសរើសទិញកញ្ចប់ {package} ។\n\n👇 សូមបញ្ជូល Username Roblox របស់អ្នកខាងក្រោម៖\n\n🚫 វាយ /cancel ដើម្បីបោះបង់។",
        'username_received_insufficient': "✅ ទទួលបាន Username: {username} ជោគជ័យ!\n\nអ្នកមិនមានលុយគ្រប់គ្រាន់ដើម្បីទិញទេ សូមធ្វើការដាក់ប្រាក់ 🤍🙏🏻",
        'username_received_success': "✅ ទទួលបាន Username: {username} ជោគជ័យ!\n\n✅ ទឹកប្រាក់ត្រូវបានកាត់ចេញពីគណនី! បញ្ជាទិញជោគជ័យ សូមរង់ចាំទទួលកូដ។",
        'lang_changed': "ភាសាត្រូវបានផ្លាស់ប្តូរទៅជា ខ្មែរ 🇰🇭", 'main_menu_text': "ត្រឡប់មកម៉ឺនុយដើម៖"
    },
    'en': {
        'welcome': "Hello {name}! Please select a service below:",
        'select_below': "👇 Please select an option below:",
        'btn_manage': "👨🏻‍💻 Manage Account", 'btn_rent': "🛍 Service Shop", 'btn_deposit': "💰 Deposit", 'btn_change_lang': "🌐 ភាសា", 
        'account_info': "👨🏻‍💻Account Info \n🌸➖➖➖➖🌸➖➖➖🌸\n  👨🏻‍💻 Name : {name}\n  🆔 ID : <code>{id}</code>\n🌸\n  💼 Balance : <b>${balance:.2f}</b>\n  🌟 Rank : Member\n🌸➖➖➖➖🌸➖➖➖🌸",
        'rent_menu_text': "Please select a service you want below:",
        'btn_robux': "🎮 Roblox Code", 'btn_back': "🔙 Back",
        'deposit_text': "Please select the amount you want to deposit:",
        'btn_custom_amount': "✍️ Custom Amount",
        'custom_amount_prompt': "👇 Enter amount (e.g., 1.50):\n\n🚫 Type /cancel to abort.",
        'generating_khqr': "⏳ Generating KHQR for {amount}...",
        'khqr_ready': "✅ Here is your KHQR for {amount}. Auto-delete in 3 mins.\n\n👇 Send receipt here.\n\n🚫 Type /cancel to abort.",
        'receipt_received': "✅ Receipt received! Wait for Admin.",
        'cancelled': "🚫 Cancelled. Back to Main Menu:",
        'robux_text': "Pricing table for Roblox Code :",
        'robux_selected': "You selected {package}.\n\n👇 Enter Roblox Username:\n\n🚫 Type /cancel to abort.",
        'username_received_insufficient': "✅ Username: {username} received!\n\nYou do not have enough balance, please deposit 🤍🙏🏻",
        'username_received_success': "✅ Username: {username} received!\n\n✅ Balance deducted! Wait for code.",
        'lang_changed': "Language changed to English 🇬🇧", 'main_menu_text': "Back to Main Menu:"
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
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(InlineKeyboardButton("$1.00", callback_data='dep_1.00'), InlineKeyboardButton("$2.00", callback_data='dep_2.00'), InlineKeyboardButton("$3.00", callback_data='dep_3.00'), InlineKeyboardButton("$4.00", callback_data='dep_4.00'), InlineKeyboardButton("$5.00", callback_data='dep_5.00'))
    markup.row(InlineKeyboardButton(texts[lang]['btn_custom_amount'], callback_data='dep_custom'))
    return markup

def get_robux_pricing_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    for key, data in robux_db.items():
        markup.add(InlineKeyboardButton(f"🪙 {data['name']} - ${data['price']:.2f}", callback_data=key))
    return markup

def delete_message_timer(chat_id, message_id):
    try: bot.delete_message(chat_id, message_id)
    except: pass 

@bot.message_handler(commands=['start'])
def send_welcome(message):
    track_user(message.from_user)
    bot.send_photo(message.chat.id, photo="https://img.sanishtech.com/u/23589ed30a9f482112e591c0f4c9fa18.png", caption=texts[get_user_lang(message.chat.id)]['welcome'].format(name=message.from_user.first_name), reply_markup=get_main_keyboard(get_user_lang(message.chat.id)))

# ================= ផ្នែក ADMIN PANEL (/admin) =================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id != ADMIN_GROUP_ID and message.from_user.id != ADMIN_USER_ID:
        # ប្តូរសារនៅទីនេះតាមការស្នើសុំ
        bot.reply_to(message, "❌ អ្នកមិនមែនជាអ្នកគ្រប់គ្រងទេ")
        return

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("📣 សារទៅទាំងអស់គ្នា", callback_data="adm_sys_broadcast"), InlineKeyboardButton("👥 ឆែកអ្នកប្រើប្រាស់", callback_data="adm_sys_users"))
    markup.add(InlineKeyboardButton("➕ បន្ថែមប្រាក់", callback_data="adm_sys_addbal"), InlineKeyboardButton("➖ ដកប្រាក់", callback_data="adm_sys_subbal"))
    markup.add(InlineKeyboardButton("✏️ កែប្រែតម្លៃ Robux", callback_data="adm_sys_editrobux")) 
    bot.reply_to(message, "🛠 <b>មឺនុយគ្រប់គ្រង (Admin Panel)</b>", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('adm_sys_'))
def handle_admin_system(call):
    action = call.data.split('_')[-1]
    bot.answer_callback_query(call.id)
    
    if action == 'users':
        if not users_db: return bot.send_message(call.message.chat.id, "📭 មិនទាន់មានអ្នកប្រើប្រាស់នៅឡើយទេ។")
        text = "👥 <b>បញ្ជីអ្នកប្រើប្រាស់ទាំងអស់:</b>\n\n"
        for uid, data in users_db.items(): text += f"🆔 <code>{uid}</code>\n👤 {data['first_name']} (@{data['username']})\n💰 Balance: <b>${data['balance']:.2f}</b>\n〰️〰️〰️〰️\n"
        bot.send_message(call.message.chat.id, text[:4000], parse_mode="HTML")
            
    elif action == 'broadcast':
        msg = bot.send_message(call.message.chat.id, "✍️ <b>សូមវាយសារដែលអ្នកចង់ Broadcast:</b>\n\n<i>(វាយ /cancel ដើម្បីបោះបង់)</i>", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_broadcast)
        
    elif action in ['addbal', 'subbal']:
        action_kh = "បន្ថែម" if action == 'addbal' else "ដក"
        msg = bot.send_message(call.message.chat.id, f"✍️ សូមបញ្ចូល <b>ID</b> របស់អ្នកប្រើប្រាស់ដែលអ្នកចង់ <b>{action_kh}</b> ប្រាក់៖\n\n<i>🚫 វាយ /cancel ដើម្បីបោះបង់។</i>", parse_mode="HTML")
        bot.register_next_step_handler(msg, lambda m: ask_amount_for_balance(m, action))
        
    elif action == 'editrobux':
        markup = InlineKeyboardMarkup(row_width=1)
        for key, data in robux_db.items():
            markup.add(InlineKeyboardButton(f"កែប្រែ: {data['name']} (${data['price']:.2f})", callback_data=f"adm_edit_rbx_{key}"))
        bot.send_message(call.message.chat.id, "⚙️ <b>សូមជ្រើសរើសកញ្ចប់ Robux ដែលអ្នកចង់កែប្រែ៖</b>", parse_mode="HTML", reply_markup=markup)

def process_broadcast(message):
    if message.text == '/cancel': return bot.send_message(message.chat.id, "🚫 បោះបង់ការផ្ញើសារ Broadcast។")
    success = 0
    bot.send_message(message.chat.id, "⏳ កំពុងធ្វើការផ្ញើ...")
    for uid in users_db.keys():
        try: bot.send_message(uid, f"📣 <b>សារជូនដំណឹងពី Admin:</b>\n\n{message.text}", parse_mode="HTML"); success += 1
        except: pass
    bot.send_message(message.chat.id, f"✅ ការ Broadcast ទទួលបានជោគជ័យ!\n👥 បានផ្ញើទៅកាន់: <b>{success} នាក់</b>", parse_mode="HTML")

def ask_amount_for_balance(message, action):
    if message.text == '/cancel': return bot.send_message(message.chat.id, "🚫 បោះបង់ប្រតិបត្តិការ។")
    try:
        target_id = int(message.text)
        if target_id not in users_db: return bot.send_message(message.chat.id, "❌ រកមិនឃើញ ID អ្នកប្រើប្រាស់នេះក្នុងប្រព័ន្ធទេ។")
        action_kh = "បន្ថែម" if action == 'addbal' else "ដក"
        msg = bot.send_message(message.chat.id, f"✍️ សូមបញ្ចូលចំនួនទឹកប្រាក់ដែលចង់ <b>{action_kh}</b> សម្រាប់ ID: <code>{target_id}</code>\n*(ឧ. 5.50)*", parse_mode="HTML")
        bot.register_next_step_handler(msg, lambda m: process_manual_balance(m, target_id, action))
    except ValueError: bot.send_message(message.chat.id, "❌ ID ត្រូវតែជាលេខសុទ្ធ។")

def process_manual_balance(message, user_id, action):
    if message.text == '/cancel': return bot.send_message(message.chat.id, "🚫 បោះបង់ប្រតិបត្តិការ។")
    try:
        amount = float(message.text)
        if action == 'addbal':
            users_db[user_id]['balance'] += amount
            bot.send_message(message.chat.id, f"✅ ជោគជ័យ! បន្ថែមប្រាក់ <b>${amount:.2f}</b> ចូលគណនី <code>{user_id}</code>។", parse_mode="HTML")
            bot.send_message(user_id, f"🎉 គណនីរបស់អ្នកត្រូវបានបន្ថែមទឹកប្រាក់ចំនួន **${amount:.2f}** ដោយ Admin។", parse_mode="Markdown")
        else:
            users_db[user_id]['balance'] -= amount
            bot.send_message(message.chat.id, f"✅ ជោគជ័យ! ដកប្រាក់ <b>${amount:.2f}</b> ពីគណនី <code>{user_id}</code>។", parse_mode="HTML")
            bot.send_message(user_id, f"📉 គណនីរបស់អ្នកត្រូវបានកាត់ទឹកប្រាក់ចំនួន **${amount:.2f}** ដោយ Admin។", parse_mode="Markdown")
            
    except ValueError: bot.send_message(message.chat.id, "❌ សូមបញ្ចូលជាលេខឱ្យបានត្រឹមត្រូវ។")

# ================= គ្រប់គ្រងការកែតម្លៃ ROBUX =================
@bot.callback_query_handler(func=lambda call: call.data.startswith('adm_edit_rbx_'))
def handle_edit_robux_selection(call):
    bot.answer_callback_query(call.id)
    pkg_key = call.data.replace('adm_edit_rbx_', '') 
    admin_editing_robux[call.message.chat.id] = pkg_key
    
    current_data = robux_db[pkg_key]
    msg = bot.send_message(call.message.chat.id, f"កំពុងកែប្រែ: <b>{current_data['name']}</b>\n\n✍️ សូមបញ្ចូល <b>ឈ្មោះកញ្ចប់ថ្មី</b>៖\n*(ឧទាហរណ៍: 500 Robux)*\n\n🚫 វាយ /cancel ដើម្បីបោះបង់។", parse_mode="HTML")
    bot.register_next_step_handler(msg, process_new_robux_name)

def process_new_robux_name(message):
    if message.text == '/cancel': return bot.send_message(message.chat.id, "🚫 បោះបង់ការកែប្រែ។")
    new_name = message.text
    pkg_key = admin_editing_robux.get(message.chat.id)
    robux_db[pkg_key]['name'] = new_name 
    
    msg = bot.send_message(message.chat.id, f"✅ ឈ្មោះថ្មី: <b>{new_name}</b>\n\n✍️ បន្តទៀត សូមបញ្ចូល <b>តម្លៃថ្មី (ជាលេខ)</b>៖\n*(ឧទាហរណ៍: 5.50)*", parse_mode="HTML")
    bot.register_next_step_handler(msg, process_new_robux_price)

def process_new_robux_price(message):
    if message.text == '/cancel': return bot.send_message(message.chat.id, "🚫 បោះបង់ការកែប្រែ។")
    try:
        new_price = float(message.text)
        pkg_key = admin_editing_robux.get(message.chat.id)
        robux_db[pkg_key]['price'] = new_price 
        bot.send_message(message.chat.id, f"🎉 <b>កែប្រែជោគជ័យ!</b>\nកញ្ចប់ថ្មីគឺ: <b>{robux_db[pkg_key]['name']}</b> ក្នុងតម្លៃ <b>${new_price:.2f}</b>", parse_mode="HTML")
    except ValueError:
        bot.send_message(message.chat.id, "❌ តម្លៃត្រូវតែជាលេខសុទ្ធ (ឧ. 5.50)។ ការកែប្រែបរាជ័យ។")

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
        process_khqr_generation(chat_id, f"${call.data.split('_')[1]}", lang)

def process_custom_amount(message):
    lang = get_user_lang(message.chat.id)
    if message.text == '/cancel': return bot.send_message(message.chat.id, texts[lang]['cancelled'])
    process_khqr_generation(message.chat.id, f"${message.text}", lang)

def process_khqr_generation(chat_id, amount, lang):
    loading_msg = bot.send_message(chat_id, texts[lang]['generating_khqr'].format(amount=amount))
    time.sleep(3)
    try: bot.delete_message(chat_id, loading_msg.message_id)
    except: pass
    khqr_msg = bot.send_photo(chat_id, photo="https://img.sanishtech.com/u/95f7764f8f7a67e3fd51da9a0ca17aac.jpeg", caption=texts[lang]['khqr_ready'].format(amount=amount))
    threading.Timer(180.0, delete_message_timer, args=(chat_id, khqr_msg.message_id)).start()
    bot.register_next_step_handler(khqr_msg, lambda m: process_receipt(m, amount))

def process_receipt(message, amount):
    lang = get_user_lang(message.chat.id)
    if message.text == '/cancel': return bot.send_message(message.chat.id, texts[lang]['cancelled'])
    bot.reply_to(message, texts[lang]['receipt_received'])
    
    admin_markup = InlineKeyboardMarkup()
    admin_markup.add(InlineKeyboardButton("✅ Approve", callback_data=f"adm_app_dep_{message.chat.id}_{amount.replace('$', '')}"), InlineKeyboardButton("❌ Reject", callback_data=f"adm_rej_dep_{message.chat.id}"))
    admin_markup.add(InlineKeyboardButton("💬 Reply ទៅកាន់ User", callback_data=f"adm_rep_msg_{message.chat.id}"))
    
    caption_text = f"💰 <b>សំណើដាក់ប្រាក់ថ្មី</b>\n\n👤 ឈ្មោះ: {message.from_user.first_name}\n🆔 ID: <code>{message.chat.id}</code>\n💵 ចំនួន: <b>{amount}</b>"
    if message.content_type == 'photo': bot.send_photo(ADMIN_GROUP_ID, message.photo[-1].file_id, caption=caption_text, parse_mode="HTML", reply_markup=admin_markup)
    else: bot.send_message(ADMIN_GROUP_ID, caption_text + "\n\n⚠️ <i>User មិនបានផ្ញើរូបភាពទេ!</i>", parse_mode="HTML", reply_markup=admin_markup)

# ================= ផ្នែក ROBUX =================
@bot.callback_query_handler(func=lambda call: call.data.startswith('robux_'))
def handle_robux_payment_callback(call):
    lang = get_user_lang(call.message.chat.id)
    bot.answer_callback_query(call.id)
    selected_pkg_name = f"{robux_db[call.data]['name']} (${robux_db[call.data]['price']:.2f})"
    msg = bot.send_message(call.message.chat.id, texts[lang]['robux_selected'].format(package=selected_pkg_name))
    bot.register_next_step_handler(msg, lambda m: process_robux_username(m, call.data))

def process_robux_username(message, package_key):
    track_user(message.from_user)
    lang = get_user_lang(message.chat.id)
    if message.text == '/cancel': return bot.send_message(message.chat.id, texts[lang]['cancelled'])
    
    price = robux_db[package_key]['price']
    package_name = robux_db[package_key]['name']
    
    if users_db[message.from_user.id]['balance'] >= price:
        users_db[message.from_user.id]['balance'] -= price
        bot.reply_to(message, texts[lang]['username_received_success'].format(username=message.text))
        
        admin_markup = InlineKeyboardMarkup()
        admin_markup.add(InlineKeyboardButton("✅ បានផ្ញើកូដរួចរាល់", callback_data=f"adm_don_ord_{message.chat.id}"), InlineKeyboardButton("💬 Reply ទាក់ទងទៅ User", callback_data=f"adm_rep_msg_{message.chat.id}"))
        order_text = f"🎮 <b>ការបញ្ជាទិញ Roblox Code ថ្មី</b>\n\n👤 ឈ្មោះ: {message.from_user.first_name}\n🆔 ID: <code>{message.chat.id}</code>\n📦 កញ្ចប់: <b>{package_name}</b>\n🎮 Username: <code>{message.text}</code>\n\n✅ <i>ទឹកប្រាក់ ${price:.2f} ត្រូវបានកាត់រួចរាល់។</i>"
        bot.send_message(ADMIN_GROUP_ID, order_text, parse_mode="HTML", reply_markup=admin_markup)
    else: bot.reply_to(message, texts[lang]['username_received_insufficient'].format(username=message.text))

# ================= ADMIN ACTIONS (Approve/Reject) =================
@bot.callback_query_handler(func=lambda call: call.data.startswith('adm_') and 'sys' not in call.data and 'edit' not in call.data)
def handle_admin_actions(call):
    data = call.data.split('_')
    action, type_, user_id = data[1], data[2], int(data[3])
    bot.answer_callback_query(call.id)
    
    if action == 'app' and type_ == 'dep':
        amount_val = float(data[4])
        if user_id in users_db: users_db[user_id]['balance'] += amount_val 
        bot.send_message(user_id, f"✅ សំណើដាក់ប្រាក់ចំនួន **${amount_val:.2f}** ត្រូវបានអនុម័ត!")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, f"✅ អនុម័តទឹកប្រាក់ចូលគណនី (ID: <code>{user_id}</code>) រួចរាល់។", parse_mode="HTML")
    elif action == 'rej' and type_ == 'dep':
        bot.send_message(user_id, "❌ សំណើដាក់ប្រាក់របស់អ្នកត្រូវបាន **បដិសេធ**!")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    elif action == 'don' and type_ == 'ord':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    elif action == 'rep' and type_ == 'msg':
        msg = bot.send_message(call.message.chat.id, f"✍️ សូមវាយសារទៅកាន់ User (ID: <code>{user_id}</code>):", parse_mode="HTML")
        bot.register_next_step_handler(msg, lambda m: forward_to_user(m, user_id))

def forward_to_user(message, user_id):
    if message.text != '/cancel': bot.send_message(user_id, f"📩 <b>សារពី Admin:</b>\n\n{message.text}", parse_mode="HTML")

# ================= TEXT HANDLER =================
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    track_user(message.from_user)
    lang = get_user_lang(message.chat.id)
    if message.text in [texts['kh']['btn_change_lang'], texts['en']['btn_change_lang']]:
        new_lang = 'en' if lang == 'kh' else 'kh'
        user_languages[message.chat.id] = new_lang
        bot.send_message(message.chat.id, texts[new_lang]['lang_changed'], reply_markup=get_main_keyboard(new_lang))
    elif message.text in [texts['kh']['btn_deposit'], texts['en']['btn_deposit']]:
        bot.send_message(message.chat.id, texts[lang]['deposit_text'], reply_markup=get_deposit_keyboard(lang))
    elif message.text in [texts['kh']['btn_manage'], texts['en']['btn_manage']]:
        bot.reply_to(message, texts[lang]['account_info'].format(name=message.from_user.first_name, id=message.chat.id, balance=users_db.get(message.chat.id, {}).get('balance', 0.0)), parse_mode="HTML")
    elif message.text in [texts['kh']['btn_rent'], texts['en']['btn_rent']]:
        bot.send_message(message.chat.id, texts[lang]['rent_menu_text'], reply_markup=get_rent_keyboard(lang))
    elif message.text in [texts['kh']['btn_robux'], texts['en']['btn_robux']]:
        bot.send_message(message.chat.id, texts[lang]['robux_text'], reply_markup=get_robux_pricing_keyboard())
    elif message.text in [texts['kh']['btn_back'], texts['en']['btn_back']]:
        bot.send_message(message.chat.id, texts[lang]['main_menu_text'], reply_markup=get_main_keyboard(lang))

print("Bot កំពុងដំណើរការ...")
bot.polling(none_stop=True)
