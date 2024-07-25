import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7049802781:AAFV7YnJW3doV1gzN062ChzMsCgXSlA291s"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Open WCoin", url=f"http://127.0.0.1:5000?user_id={user_id}")
    markup.add(button)
    bot.send_message(message.chat.id, "Welcome to WCoin! Click the button below to start earning coins.", reply_markup=markup)

bot.polling()
