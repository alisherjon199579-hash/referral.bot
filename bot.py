import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8755227656:AAGM1esD7NbCsWm2O1lDQQd-XN06UxYW-Tk"
ADMIN_ID = 282155346

bot = telebot.TeleBot(TOKEN)

# 📊 DATA
users = {}        # balans
all_users = set() # barcha userlar
referrals = {}    # referral

reklama_mode = {}

# 🔘 MENU
def menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👥 Taklif qilish", "💰 Balans")
    markup.add("💸 Pul chiqarish", "📦 Buyurtma berish")
    markup.add("📢 Reklama", "ℹ️ Biz haqimizda")
    return markup

# 🚀 START + REFERRAL
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    all_users.add(user_id)

    if user_id not in users:
        users[user_id] = 0

        args = message.text.split()
        if len(args) > 1:
            ref_id = int(args[1])
            if ref_id != user_id:
                users[ref_id] = users.get(ref_id, 0) + 500
                bot.send_message(ref_id, "🎉 500 so‘m qo‘shildi!")

    bot.send_message(user_id, "👋 Xush kelibsiz!", reply_markup=menu())

# 👥 TAKLIF
@bot.message_handler(func=lambda m: m.text == "👥 Taklif qilish")
def refer(message):
    link = f"https://t.me/{bot.get_me().username}?start={message.from_user.id}"
    bot.send_message(message.chat.id, f"👥 Taklif link:\n{link}")

# 💰 BALANS
@bot.message_handler(func=lambda m: m.text == "💰 Balans")
def balance(message):
    bot.send_message(message.chat.id, f"💰 Balans: {users.get(message.from_user.id,0)} so‘m")

# 💸 PUL CHIQARISH
@bot.message_handler(func=lambda m: m.text == "💸 Pul chiqarish")
def withdraw(message):
    user_id = message.from_user.id
    bal = users.get(user_id, 0)

    if bal < 20000:
        bot.send_message(message.chat.id, "❌ Minimum 20.000 so‘m kerak")
    else:
        bot.send_message(message.chat.id, "💳 Karta raqamingizni yuboring:")
        bot.register_next_step_handler(message, get_card)

def get_card(message):
    user_id = message.from_user.id
    amount = users.get(user_id, 0)
    card = message.text

    users[user_id] = 0

    bot.send_message(message.chat.id, "⏳ Tekshirilmoqda...\n✅ Tez orada to‘lov qilinadi")

    bot.send_message(ADMIN_ID, f"""
💸 PUL CHIQARISH

👤 ID: {user_id}
💳 Karta: {card}
💰 {amount} so‘m
""")

# 📦 BUYURTMA
@bot.message_handler(func=lambda m: m.text == "📦 Buyurtma berish")
def order(message):
    bot.send_message(message.chat.id, "📍 Manzil yozing:")
    bot.register_next_step_handler(message, get_address)

def get_address(message):
    address = message.text
    bot.send_message(message.chat.id, "📞 Telefon yozing:")
    bot.register_next_step_handler(message, finish_order, address)

def finish_order(message, address):
    phone = message.text

    bot.send_message(message.chat.id, "✅ Buyurtma qabul qilindi!")

    bot.send_message(ADMIN_ID, f"""
📦 YANGI BUYURTMA

📍 {address}
📞 {phone}
👤 {message.from_user.id}
""")

# 📢 REKLAMA (MATN)
@bot.message_handler(commands=['reklama'])
def reklama(message):
    if message.from_user.id != ADMIN_ID:
        return

    text = message.text.replace("/reklama ", "")
    count = 0

    for user_id in all_users:
        try:
            bot.send_message(user_id, text)
            count += 1
        except:
            pass

    bot.send_message(message.chat.id, f"✅ {count} ta odamga yuborildi")

# 📸 FOTO REKLAMA
@bot.message_handler(commands=['reklama_photo'])
def reklama_photo(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    reklama_mode[message.from_user.id] = True
    bot.send_message(message.chat.id, "📸 Rasm yuboring (caption bilan)")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.from_user.id not in reklama_mode:
        return

    photo = message.photo[-1].file_id
    caption = message.caption if message.caption else ""

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📦 Buyurtma berish", url=f"https://t.me/{bot.get_me().username}"))

    count = 0

    for user_id in all_users:
        try:
            bot.send_photo(user_id, photo, caption, reply_markup=markup)
            count += 1
        except:
            pass

    bot.send_message(message.chat.id, f"✅ {count} ta odamga yuborildi")
    reklama_mode.pop(message.from_user.id)

# ℹ️ ABOUT
@bot.message_handler(func=lambda m: m.text == "ℹ️ Biz haqimizda")
def about(message):
    bot.send_message(message.chat.id, """
🏢 TOZA GILAM

📍 G‘ijduvon
📞 +998 90 123 45 67

🚀 Sifatli xizmat
""")

print("🚀 BOT ISHLADI...")
bot.polling()
