# Updater — компонент отвечающий за коммуникацию с сервером Telegram, т.е. за получение и передачу сообщения.
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from settings import TG_TOKEN
from telegram import ReplyKeyboardMarkup

#функция parrot отвечает тем же сообщением, которое ему прислали (П:Привет! Б:Привет!)
#функция sms вызывается пользователем при отправке команды, к которой эта функция привязана
def sms_start(bot, update):
    print('start')
    bot.message.reply_text('Привет, {}! \nТы здесь, потому что хочешь найти ментора или хочешь стать им. \nПозволь мне помочь!'.format(bot.message.chat.first_name))
    print(bot.message)
    keyboard_side = ReplyKeyboardMarkup([['Найти ментора'], ['Стать ментором']])
    bot.message.reply_text('Хочешь найти ментора или стать ментором?', reply_markup=keyboard_side)




# Создаем main, которая соединяется с Telegram. Main-тело программы, содержит в себе описание действий
def main():
    my_bot = Updater(TG_TOKEN)

    my_bot.dispatcher.add_handler(CommandHandler('start', sms_start))

    my_bot.start_polling()
    my_bot.idle()

main()
