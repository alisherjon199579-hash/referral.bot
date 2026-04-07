import telebot
from telebot import types

TOKEN = "7624922503:AAHeCFszGZaj13M6xvNWOjMVT6VxbfJlSuM" 

bot = telebot.TeleBot(TOKEN)

# 📊 Ma'lumotlar
users = {}
referrals = {}
balance = {}

# 🚀 START
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    args = message.text.split()

    # yangi user
    if user_id not in users:
        users[user_id] = True
        balance[user_id] = 0

        # referral bo‘lsa
        if len(args) > 1:
            ref_id = int(args[1])

            if ref_id != user_id:
                referrals[user_id] = ref_id
                balance[ref_id] += 500

                bot.send_message(ref_id, "🎉 Sizga 500 so‘m qo‘shildi!")

    # 🔘 MENU
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👥 Taklif qilish", "💰 Balans")

    bot.send_message(user_id, "👋 Xush kelibsiz!", reply_markup=markup)

# 👥 TAKLIF LINK
@bot.message_handler(func=lambda m: m.text == "👥 Taklif qilish")
def invite(message):
    link = f"https://t.me/{bot.get_me().username}?start={message.chat.id}"
    bot.send_message(message.chat.id, f"👥 Do‘stlaringizni taklif qiling:\n{link}")

# 💰 BALANS
@bot.message_handler(func=lambda m: m.text == "💰 Balans")
def show_balance(message):
    bal = balance.get(message.chat.id, 0)
    bot.send_message(message.chat.id, f"💰 Sizning balansingiz: {bal} so‘m")

print("🚀 Referral bot ishga tushdi...")
bot.polling()
