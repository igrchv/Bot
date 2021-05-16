# Updater — компонент отвечающий за коммуникацию с сервером Telegram, т.е. за получение и передачу сообщения.
from telegram.ext import Updater
# CommandHandler  управляет функциями на основе команд, полученных из телеги
from telegram.ext import CommandHandler
# MessageHadler управляет функциями на основе сообщений, отправленных юзером (для кнопок)
from telegram.ext import MessageHandler
# Filters.text указывает, какой тип сообщения обрабатывать
from telegram.ext import Filters
# TG_TOKEN импортирует из settings.py токен бота
from settings import TG_TOKEN
# ReplyKeyboardMarkup - модуль разметки клавиатуры.
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardRemove


# функция parrot отвечает тем же сообщением, которое ему прислали (П:Привет! Б:Привет!)
# функция sms вызывается пользователем при отправке команды, к которой эта функция привязана

# Начало работы, вопрос кем хочет быть в виде кнопок
def sms_start(bot, update):
    print('\n\nНачало')
    bot.message.reply_text('Привет, {}! \nТы здесь, потому что хочешь найти ментора или хочешь стать им. \nПозволь мне помочь!'.format(bot.message.chat.first_name))
    print(bot.message)
    keyboard_side = ReplyKeyboardMarkup([['Найти ментора'], ['Стать ментором']])
    bot.message.reply_text('Хочешь найти ментора или стать ментором?', reply_markup=keyboard_side)

#________________________________________________________________________________________________________________________________________________________________________
# Анкета ментора
def mentor_anketa_start(bot, update):
    print('\nХочешь найти ментора или стать ментором?')
    print(bot.message.text)
    keyboard_mentor_anketa = ReplyKeyboardMarkup([['Карьерный рост'], ['Личностная эффективность'],
                                                  ['Профессиональное развитие']])
    bot.message.reply_text('Отлично! \nТеперь выбери сферу, в которой хочешь быть ментором.',
                            reply_markup=keyboard_mentor_anketa) # задаем вопрос и выводим клавиатуру
    return "Сфера" # ключ для определения следующего шага

def mentor_anketa_sfera(bot, update):
    print('\nСфера:')
    print(bot.message.text)
    update.user_data['Сфера'] = bot.message.text #временно сохраняем ответ
    bot.message.reply_text("Готово! \nПросматривайте анкеты и выбирайте достоных кандидатов.")
    return ConversationHandler.END #выходим из диалога
#____________________________________________________________________________________________________________
# Анкета Менти
def mentee_anketa_start(bot, update):
    print('\nХочешь найти ментора или стать ментором?')
    print(bot.message.text)
    bot.message.reply_text('Отлично! \nТеперь тебе надо заполнить анкету.')
    keyboard_anketa = ReplyKeyboardMarkup([['Карьерный рост'], ['Личностная эффективность'],
                                           ['Профессиональное развитие']])
    bot.message.reply_text('Для начала, выбери сферу, в которой тебе нужен ментор.', reply_markup=keyboard_anketa)
    return "Сфера"

def mentee_anketa_sfera(bot, update):
    update.user_data['Сфера'] = bot.message.text
    bot.message.reply_text('Введи свои имя и фамилию. \nНапример, вот так: Иван Иванов', reply_markup=ReplyKeyboardRemove())
    return "Имя"

def mentee_anketa_name(bot, update):
    update.user_data['Имя'] = bot.message.text
    bot.message.reply_text('Введи свою должность.')
    return "Должность"

def mentee_anketa_position(bot, update):
    update.user_data['Должность'] = bot.message.text
    bot.message.reply_text('Напиши, почему ты хочешь найти ментора.')
    return "Мотивация"

def mentee_anketa_motivation(bot, update):
    update.user_data['Мотивация'] = bot.message.text
    text = """Имя:{Имя}
    Сфера: {Сфера}
    Должность: {Должность}
    Мотивация: {Мотивация}""".format(**update.user_data) #** в форматировании подставляют значения
    bot.message.reply_text(text)
    keyboard_MenteeCheck = ReplyKeyboardMarkup([['Все верно'],['Пройти заново']])
    bot.message.reply_text('Проверь анкету на корректность информации.', reply_markup=keyboard_MenteeCheck)
    return "Конец анкеты"

def mentee_anketa_end(bot, update):
    text = """Имя: {Имя}
    Сфера: {Сфера}
    Должность: {Должность}
    Мотивация: {Мотивация}""".format(**update.user_data)
    print('\n',text)
    bot.message.reply_text('Готово, теперь менторы смогут увидеть твою анкету.'
                           '\nЕсли хочешь оставить анкету в другой сфере, напиши /start', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

# Выбор сферы в случае, если "Стать ментором"
#def mentor_sfera(bot, update):
#    print('\nХочешь найти ментора или стать ментором?')
#    print(bot.message.text)
#    keyboard_anketa_mentor = ReplyKeyboardMarkup([['Карьерный рост'], ['Личностная эффективность'],
#                                           ['Профессиональное развитие']])
#    bot.message.reply_text('Отлично! \nТеперь выбери сферу, в которой хочешь быть ментором',
#                           reply_markup=keyboard_anketa_mentor)



# Начало анкеты (сфера) в случае, если "Найти ментора"
#def anketa_sfera(bot, update):
#    print('\nХочешь найти ментора или стать ментором?')
#    print(bot.message.text)
#    bot.message.reply_text('Отлично! \nТеперь тебе надо заполнить анкету.')
#    keyboard_anketa = ReplyKeyboardMarkup([['Карьерный рост'], ['Личностная эффективность'],
#                                           ['Профессиональное развитие']])
#    bot.message.reply_text('Для начала, выбери сферу, в которой тебе нужен ментор', reply_markup=keyboard_anketa)

# Имя Фамилия "Найти ментора"
#def anketa_name(bot, update):
#    print('Имя, фамилия: ')
#    bot.message.reply_text('Введи свои имя и фамилию. \nНапример, вот так: Иван Иванов')
#    print(bot.message.text)

# Должность "Найти ментора"
#def anketa_position(bot, update):
#    print('Должность: ')
#    bot.message.reply_text('Введи свою должность')
#    print(bot.message.text)


# Создаем main, которая соединяется с Telegram. Main-тело программы, содержит в себе описание действий
def main():
    my_bot = Updater(TG_TOKEN)

    my_bot.dispatcher.add_handler(CommandHandler('start', sms_start))

# Анкета "Стать ментором"
    my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex('Стать ментором'), mentor_anketa_start)],
                                                      states={
                                                          "Сфера": [MessageHandler(Filters.regex('Карьерный рост|Личностная эффективность|Профессиональное развитие'), mentor_anketa_sfera)]
                                                      },
                                                      fallbacks=[]
                                                      )
                                  )
# Анкета "Найти ментора"
    my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex('Найти ментора'), mentee_anketa_start)],
                                                      states={
                                                          "Сфера": [MessageHandler(Filters.regex('Карьерный рост|Личностная эффективность|Профессиональное развитие'), mentee_anketa_sfera)],
                                                          "Имя": [MessageHandler(Filters.text, mentee_anketa_name)],
                                                          "Должность": [MessageHandler(Filters.text, mentee_anketa_position)],
                                                          "Мотивация": [MessageHandler(Filters.text, mentee_anketa_motivation)],
                                                          "Конец анкеты": [MessageHandler(Filters.regex('Все верно'), mentee_anketa_end),
                                                                           MessageHandler(Filters.regex('Пройти заново'), mentee_anketa_start)]
                                                      },
                                                      fallbacks=[]
                                                      )
                                  )

#    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Найти ментора'), anketa_sfera))
#    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Стать ментором'), mentor_sfera))

#    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Карьерный рост'), anketa_name))
#    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Личностная эффективность'), anketa_name))
#    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Профессиональное развитие'), anketa_name))

#    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, anketa_position))
#    if Filters.text = True

    my_bot.start_polling()
    my_bot.idle()

main()
