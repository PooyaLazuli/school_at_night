import telebot


bot = telebot.TeleBot("8019401106:AAEyA5G8q2u_mk7SXDxQfkzfaTgVkNo_1RQ")

@bot.message_handler(commands=['start','help'])

def start(msg):
    bot.send_message(msg.chat.id,"سلام کوچه ای")

bot.infinity_polling()

