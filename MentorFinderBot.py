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
from telegram import ParseMode
import sqlite3


# функция parrot отвечает тем же сообщением, которое ему прислали (П:Привет! Б:Привет!)
# функция sms вызывается пользователем при отправке команды, к которой эта функция привязана

# База данных
conn = sqlite3.connect('db/database_mentee.db', check_same_thread=False)
cursor = conn.cursor()

def db_enter(user_id: int, user_name:str, user_sphere:str, user_job:str, user_motivation:str,  username:str, job_description:str):
    cursor.execute('INSERT INTO mentee (user_id, user_name, user_sphere, user_job, user_motivation, username, job_description) VALUES (?,?,?,?,?,?,?)',
                   (user_id, user_name, user_sphere, user_job, user_motivation, username, job_description))
    conn.commit()

#user_name:str, user_sphere:str, user_job:str, user_motivation:str,
# user_name, user_sphere, user_job, user_motivation,
# ,?,?,?

# Начало работы, вопрос кем хочет быть в виде кнопок
def sms_start(bot, update):
    print('\n\nНачало')
    bot.message.reply_text('Здравствуйте, {}! \nВы здесь, потому что хотите найти ментора или хотите стать им. \nПозвольте мне помочь!'
                           '\nЧтобы начать заново, напишите \n/start'
                           '\nЧтобы посмотреть свои анкеты, напишите \n/my_profile'.format(bot.message.chat.first_name))
    print(bot.message)
    keyboard_side = ReplyKeyboardMarkup([['Найти ментора'], ['Стать ментором']])
    bot.message.reply_text('Хотите найти ментора или стать ментором?', reply_markup=keyboard_side)

#________________________________________________________________________________________________________________________________________________________________________
# Анкета ментора
# можнр вывести анкету с id#1 отдельной функцией, присвоив аргумент. Последующие анкеты будут показаны с помощью отдельной функции, где id=id+1
# или сделать 3 таблицы?
def mentor_anketa_start(bot, update):
    print('\nХочешь найти ментора или стать ментором?')
    print(bot.message.text)
    keyboard_mentor_anketa = ReplyKeyboardMarkup([['Карьерный рост'], ['Личная эффективность'],
                                                  ['Профессиональное развитие']])
    bot.message.reply_text('Отлично! \nТеперь выберите сферу, в которой хотите быть ментором.',
                            reply_markup=keyboard_mentor_anketa) # задаем вопрос и выводим клавиатуру
    return "Сфера" # ключ для определения следующего шага

def mentor_anketa_sfera(bot, update):
    print('\nСфера:')
    print(bot.message.text)
    update.user_data['sphere'] = bot.message.text #временно сохраняем ответ
    keyboard_mentor_nachalo = ReplyKeyboardMarkup([['Показать анкету']], resize_keyboard=True)
    bot.message.reply_text('Готово! \nПросматривайте анкеты и выбирайте достойных кандидатов.', reply_markup=keyboard_mentor_nachalo)
    # i=0
    # update.user_data['i']=i
    return "Показ анкеты" #выходим из диалога

def mentor_show_anketa(bot,update):
    sfera1 = """{sphere}""".format(**update.user_data)
    # sfera=sfera1
    print(sfera1)
    cursor.execute("""SELECT * 
            FROM mentee 
            WHERE user_sphere=?
            ORDER BY id 
            LIMIT 1""", (sfera1,))# WHERE user_sphere="""{Сфера}""".format(update.user_data')
    info = cursor.fetchone()
    if info is None:
        keyboard_mentor_net = ReplyKeyboardMarkup([['Сменить сферу'],['Прекратить поиск']])
        bot.message.reply_text('Анкет в этой сфере нет, но Вы можете выбрать другую!',reply_markup=keyboard_mentor_net)
    else:
        record = info
        for row in record:
            update.user_data['name'] = record[1]
            update.user_data['sfera'] = record[2]
            update.user_data['job'] = record[3]
            update.user_data['motivation'] = record[4]
            update.user_data['username'] = record[5]
            id = record[6]
            update.user_data['id'] = id
            update.user_data['job_description'] = record[7]
        text = """<b>{name}</b>
<b>@{username}\n</b>
<b>Сфера:</b> {sfera}
<b>Должность:</b> {job}
<b>Описание работы:</b> {job_description}
<b>Мотивация:</b> {motivation}""".format(**update.user_data)
        cursor.execute("""SELECT id FROM mentee ORDER BY id DESC """)
        row = cursor.fetchone()
        rowitem = row[0]
        max_id = rowitem
        # print(max_id)
        max_id1 = max_id + 1
        # print(max_id1)
        cursor.execute("""UPDATE mentee SET id=? WHERE id=(SELECT id FROM mentee WHERE user_sphere=?)""", (max_id1, sfera1, ))
        conn.commit()
        keyboard_mentor_vibor = ReplyKeyboardMarkup([['Показать новую анкету'], ['Сменить сферу'],
                                                 ['Кандидат подходит'],['Прекратить поиск']])
        bot.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=keyboard_mentor_vibor)
    return "Выбор"

def mentor_end(bot,update):
    bot.message.reply_text('Кто-то только что нашел себе ментора!\nВам остается только связаться с хозяином анкеты, нажав на его юзернейм.\n'
                           'Чтобы снова посмотреть анкеты, напишите /start',
                           reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
    # username="""{username}""".format(**update.user_data)
    # sfera="""{sphere}""".format(**update.user_data)
    # motiv="""{motivation}""".format(**update.user_data)
    # job = """{job}""".format(**update.user_data)
    # description = """{job_description}""".format(**update.user_data)
    # cursor.execute("""DELETE FROM mentee WHERE username=? AND user_sphere=?""",(username, sfera))
    # conn.commit()


def mentor_exit(bot,update):
    bot.message.reply_text('Очень жаль, что ни один кандидат не подошел. Возможно, позже появятся другие анкеты.\nЕсли захотите попробовать снова, напишите /start',
                           reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
#____________________________________________________________________________________________________________
# Анкета Менти
def mentee_anketa_start(bot, update):
    print('\nХочешь найти ментора или стать ментором?')
    print(bot.message.text)
    update.user_data['username'] = bot.message.chat.username
    bot.message.reply_text('Отлично! \nТеперь Вам надо заполнить анкету. '
                           'Именно ее будут видеть менторы, поэтому укажите всю, на ваш взгляд, важную информацию!')
    keyboard_anketa = ReplyKeyboardMarkup([['Карьерный рост'], ['Личная эффективность'],
                                           ['Профессиональное развитие']])
    bot.message.reply_text('Для начала выберите сферу, в которой Вам нужен ментор.', reply_markup=keyboard_anketa)
    return "Сфера"

def mentee_anketa_sfera(bot, update):
    update.user_data['Сфера'] = bot.message.text
    # check_sfera='''{Сфера}'''.format(**update.user_data)
    check_sfera=bot.message.text#"""Сфера""".format(**update.user_data)
    username=bot.message.chat.username
    cursor.execute("""SELECT username FROM mentee WHERE user_sphere=? AND username=?""",(check_sfera,username, ))
    check_username=cursor.fetchone()
    if check_username is None:
        bot.message.reply_text('Введите свои имя и фамилию. \nНапример, вот так: Иван Иванов.',
                           reply_markup=ReplyKeyboardRemove())
        return "Имя"
    else:
        bot.message.reply_text('Вы уже оставляли анкету! Вот она:', reply_markup=ReplyKeyboardRemove())
        cursor.execute("""SELECT * FROM mentee WHERE user_sphere=? AND username=?""", (check_sfera, username, ))
        record = cursor.fetchone()
        for row in record:
            update.user_data['name'] = record[1]
            update.user_data['sfera'] = record[2]
            update.user_data['job'] = record[3]
            update.user_data['motivation'] = record[4]
            update.user_data['юзернейм'] = record[5]
            update.user_data['job_description'] = record[7]
        text = """<b>{name}</b>
<b>@{юзернейм}\n</b>
<b>Сфера:</b> {sfera}
<b>Должность:</b> {job}
<b>Описание работы:</b> {job_description}
<b>Мотивация:</b> {motivation}""".format(**update.user_data)
        bot.message.reply_text(text, parse_mode=ParseMode.HTML)
        bot.message.reply_text('Если хотите оставить анкету в другой сфере, напишите /start'
                               '\nЕсли хотите изменить или удалить анкету, напишите /my_profile')
        return ConversationHandler.END

def mentee_anketa_name(bot, update):
    update.user_data['Имя'] = bot.message.text
    bot.message.reply_text('Введите свою должность.')
    return "Должность"

def mentee_anketa_position(bot, update):
    update.user_data['Должность'] = bot.message.text
    bot.message.reply_text('Напишите подробнее про свою работу')
    return "Описание работы"

def mentee_anketa_job(bot,update):
    update.user_data['Описание работы'] = bot.message.text
    bot.message.reply_text('Напишите, почему Вы хотите найти ментора.\n'
                           'Укажите ваши ожидания от помощи ментора, желаемые результаты.')
    return "Мотивация"

def mentee_anketa_motivation(bot, update):
    update.user_data['Мотивация'] = bot.message.text
    text = '''<b>{Имя}</b>
<b>\nСфера:</b> {Сфера}
<b>Должность:</b> {Должность}
<b>Описание работы:</b> {Описание работы}
<b>Мотивация:</b> {Мотивация}
    '''.format(**update.user_data) #** в форматировании подставляют значения
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)
    keyboard_MenteeCheck = ReplyKeyboardMarkup([['Все верно'],['Пройти заново']])
    bot.message.reply_text('Проверьте анкету на корректность информации.', reply_markup=keyboard_MenteeCheck)
    return "Конец анкеты"

def mentee_anketa_end(bot, update):
    text ="""username: {username}
    Имя: {Имя}
    Сфера: {Сфера}
    Должность: {Должность}
    Описание работы: {Описание работы}
    Мотивация: {Мотивация}""".format(**update.user_data)
    print('\n',text)
    bot.message.reply_text('Готово, теперь менторы смогут увидеть Вашу анкету. Не забудте удалить ее, когда с Вами свяжется ментор!'
                           '\nЕсли хотите оставить анкету в другой сфере, напишите /start'
                           '\nЕсли хотите изменить или удалить анкету, напишите /my_profile', reply_markup=ReplyKeyboardRemove())

    us_id=bot.message.chat.id
    us_name="""{Имя}""".format(**update.user_data)
    us_sphere="""{Сфера}""".format(**update.user_data)
    us_job="""{Должность}""".format(**update.user_data)
    us_opisanie="""{Описание работы}""".format(**update.user_data)
    us_motivation="""{Мотивация}""".format(**update.user_data)
    username=bot.message.chat.username

    db_enter(user_id=us_id, user_name=us_name, user_sphere=us_sphere, user_job=us_job, user_motivation=us_motivation, username=username, job_description=us_opisanie)
    conn.commit()
    return ConversationHandler.END

#_________________________________________________________________________________________________________________________________________________________________________________________
# Показ и удаление своей анкеты.

def display_anketa(bot,update):
    keyboard_display1 = ReplyKeyboardMarkup([['Карьерный рост'], ['Личная эффективность'],
                                                  ['Профессиональное развитие']])
    bot.message.reply_text('Выберите сферу, в которой оставили анкету.', reply_markup=keyboard_display1)
    return "Показать свою"

def display_anketa2(bot,update):
    display_sfera=bot.message.text
    display_username=bot.message.chat.username
    cursor.execute("""SELECT * FROM mentee WHERE user_sphere=? AND username=?""", (display_sfera, display_username,))
    display_info = cursor.fetchone()
    if display_info is None:
        bot.message.reply_text('В этой сфере Вы не оставляли анкету.\nЧтобы оставить новую анкету, напишите \n/start'
                           '\nЧтобы посмотреть свои анкеты, напишите \n/my_profile', reply_markup=ReplyKeyboardRemove())
    else:
        record = display_info
        for row in record:
            update.user_data['name'] = record[1]
            update.user_data['sfera'] = record[2]
            update.user_data['job'] = record[3]
            update.user_data['motivation'] = record[4]
            update.user_data['юзернейм'] = record[5]
            update.user_data['job_description'] = record[7]
        text = """<b>{name}</b>
<b>@{юзернейм}\n</b>
<b>Сфера:</b> {sfera}
<b>Должность:</b> {job}
<b>Описание работы:</b> {job_description}
<b>Мотивация:</b> {motivation}""".format(**update.user_data)
        keyboard_display2 = ReplyKeyboardMarkup([['Удалить анкету'],
                                             ['Изменить анкету'],
                                             ['Оставить без изменений']])
        bot.message.reply_text(text, parse_mode=ParseMode.HTML)
        bot.message.reply_text('Выберите, что хотите сделать со своей анкетой.', reply_markup=keyboard_display2)
    return "Показать свою 2"

def display_delete_confirmation(bot,update):
    keyboard_confirm_delete= ReplyKeyboardMarkup([['Да'],['Нет']])
    bot.message.reply_text('Вы точно хотите удалить анкету?', reply_markup=keyboard_confirm_delete)
    return "Удаление подтвердить"

def display_delete(bot,update):
    display_username = bot.message.chat.username
    display_delete_sfera = """{sfera}""".format(**update.user_data)
    cursor.execute("""DELETE FROM mentee WHERE username=? AND user_sphere=?""",
                   (display_username, display_delete_sfera,))
    conn.commit()
    bot.message.reply_text('Анкета удалена!\nЧтобы оставить новую, напишите \n/start'
                           '\nЧтобы посмотреть свои анкеты в других сферах, напишите \n/my_profile', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def display_delete_reject(bot,update):
    bot.message.reply_text('Хорошо, менторы и дальше смогут видеть Вашу анкету.\nЧтобы оставить анкету в другой сфере, напишите \n/start'
                           '\nЧтобы посмотреть свои анкеты в других сферах, напишите \n/my_profile',
                           reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def display_leave(bot,update):
    bot.message.reply_text('Поиски продолжаются!'
                           '\nЧтобы оставить анкету в другой сфере, напишите:\n/start'
                           '\nЧтобы изменить или удалить анкету, напишите:\n/my_profile', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def display_change(bot, update):
    update.user_data['Сфера изменение'] = """{sfera}""".format(**update.user_data)
    # check_sfera='''{Сфера}'''.format(**update.user_data)
    # check_sfera=bot.message.text#"""Сфера""".format(**update.user_data)
    # username=bot.message.chat.username
    # cursor.execute("""SELECT username FROM mentee WHERE user_sphere=?""",(check_sfera,))
    # check_username=cursor.fetchone()
    # if check_username is None:
    bot.message.reply_text('Введите свои имя и фамилию. \nНапример, вот так: Иван Иванов',
                           reply_markup=ReplyKeyboardRemove())
    return "Имя изменение"
#     else:
#         bot.message.reply_text('Вы уже оставляли анкету! Вот она:', reply_markup=ReplyKeyboardRemove())
#         cursor.execute("""SELECT * FROM mentee WHERE user_sphere=? AND username=?""", (check_sfera, username, ))
#         record = cursor.fetchone()
#         for row in record:
#             update.user_data['name'] = record[1]
#             update.user_data['sfera'] = record[2]
#             update.user_data['job'] = record[3]
#             update.user_data['motivation'] = record[4]
#             update.user_data['юзернейм'] = record[5]
#             update.user_data['job_description'] = record[7]
#         text = """<b>{name}</b>
# <b>@{юзернейм}\n</b>
# <b>Сфера:</b> {sfera}
# <b>Должность:</b> {job}
# <b>Описание работы:</b> {job_description}
# <b>Мотивация:</b> {motivation}""".format(**update.user_data)
#         bot.message.reply_text(text, parse_mode=ParseMode.HTML)
#         bot.message.reply_text('Если хотите оставить анкету в другой сфере, напишите /start'
#                                '\nЕсли хотите изменить или удалить анкету, напишите /my_profile')
#         return ConversationHandler.END

def display_change_name(bot, update):
    update.user_data['Имя изменение'] = bot.message.text
    bot.message.reply_text('Введите свою должность.')
    return "Должность изменение"

def display_change_position(bot, update):
    update.user_data['Должность изменение'] = bot.message.text
    bot.message.reply_text('Напишите подробнее про свою работу.')
    return "Описание работы изменение"

def display_change_job(bot,update):
    update.user_data['Описание работы изменение'] = bot.message.text
    bot.message.reply_text('Напишите, почему Вы хотите найти ментора.\n'
                           'Укажите ваши ожидания от помощи ментора, желаемые результаты.')
    return "Мотивация изменение"

def display_change_motivation(bot, update):
    update.user_data['Мотивация изменение'] = bot.message.text
    text = '''<b>{Имя изменение}</b>
<b>\nСфера:</b> {Сфера изменение}
<b>Должность:</b> {Должность изменение}
<b>Описание работы:</b> {Описание работы изменение}
<b>Мотивация:</b> {Мотивация изменение}
    '''.format(**update.user_data) #** в форматировании подставляют значения
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)
    keyboard_displayMenteeCheck = ReplyKeyboardMarkup([['Все верно'],['Пройти заново']])
    bot.message.reply_text('Проверьте анкету на корректность информации.', reply_markup=keyboard_displayMenteeCheck)
    return "Конец анкеты изменение"

def display_change_end(bot, update):
    text ="""username: {юзернейм}
Имя: {Имя изменение}
Сфера: {Сфера изменение}
Должность: {Должность изменение}
Описание работы: {Описание работы изменение}
Мотивация: {Мотивация изменение}""".format(**update.user_data)
    print('\n',text)
    bot.message.reply_text('Готово, теперь менторы смогут увидеть Вашу обновленную анкету.'
                           '\nЕсли хотите оставить анкету в другой сфере, напишите /start'
                           '\nЕсли хотите изменить или удалить анкету, напишите /my_profile', reply_markup=ReplyKeyboardRemove())

    # us_id=bot.message.chat.id
    us_name_chage="""{Имя изменение}""".format(**update.user_data)
    us_sphere="""{Сфера изменение}""".format(**update.user_data)
    us_job_change="""{Должность изменение}""".format(**update.user_data)
    us_opisanie_change="""{Описание работы изменение}""".format(**update.user_data)
    us_motivation_change="""{Мотивация изменение}""".format(**update.user_data)
    username=bot.message.chat.username
    cursor.execute("""UPDATE mentee SET user_name=?, user_job=?, user_motivation=?, job_description=? WHERE username=? AND user_sphere=?""",
                   (us_name_chage, us_job_change, us_motivation_change, us_opisanie_change, username, us_sphere))
    # db_enter(user_id=us_id, user_name=us_name, user_sphere=us_sphere, user_job=us_job, user_motivation=us_motivation, username=username, job_description=us_opisanie)
    conn.commit()
    return ConversationHandler.END

# user_name=us_name, user_job=us_job, useяr_motivation=us_motivation,

# Создаем main, которая соединяется с Telegram. Main-тело программы, содержит в себе описание действий
def main():
    my_bot = Updater(TG_TOKEN)

    my_bot.dispatcher.add_handler(CommandHandler('start', sms_start))

# Анкета "Стать ментором"
    my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex('Стать ментором'), mentor_anketa_start)],
                                                      states={
                                                          "Сфера": [MessageHandler(Filters.regex('Карьерный рост|Личная эффективность|Профессиональное развитие'), mentor_anketa_sfera)],
                                                          "Показ анкеты": [MessageHandler(Filters.regex('Показать анкету'), mentor_show_anketa)],
                                                          "Выбор": [MessageHandler(Filters.regex('Показать новую анкету'), mentor_show_anketa),
                                                                    MessageHandler(Filters.regex('Сменить сферу'), mentor_anketa_start),
                                                                    MessageHandler(Filters.regex('Кандидат подходит'), mentor_end),
                                                                    MessageHandler(Filters.regex('Прекратить поиск'), mentor_exit)]
                                                      },
                                                      fallbacks=[],
                                                      allow_reentry=True
                                                      )
                                  )
# Анкета "Найти ментора"
    my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex('Найти ментора'), mentee_anketa_start)],
                                                      states={
                                                          "Сфера": [MessageHandler(Filters.regex('Карьерный рост|Личная эффективность|Профессиональное развитие'), mentee_anketa_sfera)],
                                                          "Имя": [MessageHandler(Filters.text, mentee_anketa_name)],
                                                          "Должность": [MessageHandler(Filters.text, mentee_anketa_position)],
                                                          "Описание работы": [MessageHandler(Filters.text, mentee_anketa_job)],
                                                          "Мотивация": [MessageHandler(Filters.text, mentee_anketa_motivation)],
                                                          "Конец анкеты": [MessageHandler(Filters.regex('Все верно'), mentee_anketa_end),
                                                                           MessageHandler(Filters.regex('Пройти заново'), mentee_anketa_start)]
                                                      },
                                                      fallbacks=[],
                                                      allow_reentry=True
                                                      )
                                  )

    my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[CommandHandler('my_profile', display_anketa)],
                                                      states={
                                                          "Показать свою": [MessageHandler(Filters.regex('Карьерный рост|Личная эффективность|Профессиональное развитие'), display_anketa2)],
                                                          "Показать свою 2": [MessageHandler(Filters.regex('Удалить анкету'), display_delete_confirmation),
                                                                              MessageHandler(Filters.regex('Оставить без изменений'), display_leave),
                                                                              MessageHandler(Filters.regex('Изменить анкету'), display_change)],
                                                          "Удаление подтвердить": [MessageHandler(Filters.regex('Да'), display_delete),
                                                                                   MessageHandler(Filters.regex('Нет'), display_delete_reject)],
                                                          "Имя изменение": [MessageHandler(Filters.text, display_change_name)],
                                                          "Должность изменение": [MessageHandler(Filters.text, display_change_position)],
                                                          "Описание работы изменение": [MessageHandler(Filters.text, display_change_job)],
                                                          "Мотивация изменение": [MessageHandler(Filters.text, display_change_motivation)],
                                                          "Конец анкеты изменение": [MessageHandler(Filters.regex('Все верно'),display_change_end),
                                                                                     MessageHandler(Filters.regex('Пройти заново'),display_change)]
                                                      },
                                                      fallbacks=[],
                                                      allow_reentry=True
                                                      )
                                  )

    my_bot.start_polling()
    my_bot.idle()

main()


# Выбор сферы в случае, если "Стать ментором"
#def mentor_sfera(bot, update):
#    print('\nХочешь найти ментора или стать ментором?')
#    print(bot.message.text)
#    keyboard_anketa_mentor = ReplyKeyboardMarkup([['Карьерный рост'], ['Личная эффективность'],
#                                           ['Профессиональное развитие']])
#    bot.message.reply_text('Отлично! \nТеперь выбери сферу, в которой хочешь быть ментором',
#                           reply_markup=keyboard_anketa_mentor)



# Начало анкеты (сфера) в случае, если "Найти ментора"
#def anketa_sfera(bot, update):
#    print('\nХочешь найти ментора или стать ментором?')
#    print(bot.message.text)
#    bot.message.reply_text('Отлично! \nТеперь тебе надо заполнить анкету.')
#    keyboard_anketa = ReplyKeyboardMarkup([['Карьерный рост'], ['Личная эффективность'],
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



#    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Найти ментора'), anketa_sfera))
#    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Стать ментором'), mentor_sfera))

#    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Карьерный рост'), anketa_name))
#    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Личная эффективность'), anketa_name))
#    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Профессиональное развитие'), anketa_name))

#    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, anketa_position))

#    if Filters.text = True

# def mentor_next(bot, update):
#     # last_user='{last_user}'.format(update.user_data)
#     # last_user=last_user+1
#     # update.user_data['last_user'] = last_user
#     sfera = """{sphere}""".format(**update.user_data)
#     cursor.execute("""SELECT *
#         FROM mentee
#         WHERE user_sphere=?
#         ORDER BY id
#         LIMIT 1""", (sfera,))  # WHERE user_sphere="""{Сфера}""".format(update.user_data')
#     record = cursor.fetchone()
#     for row in record:
#         update.user_data['name'] = record[1]
#         update.user_data['sfera'] = record[2]
#         update.user_data['job'] = record[3]
#         update.user_data['motivation'] = record[4]
#         update.user_data['username'] = record[5]
#         id=record[6]
#         update.user_data['id'] = id
#     text = """{name}
# @{username}\n
# Сфера: {sfera}
# Должность: {job}
# Мотивация: {motivation}""".format(**update.user_data)
#     cursor.execute("""SELECT id FROM mentee ORDER BY id DESC """)
#     row=cursor.fetchone()
#     rowitem=row[0]
#     max_id=rowitem
#     print(max_id)
#     max_id1=max_id+1
#     print(max_id1)
#     cursor.execute("""UPDATE mentee SET id=? WHERE id=(SELECT id FROM  mentee ORDER BY id ASC )""", (max_id1,))
#     conn.commit()
#     keyboard_mentor_vibor = ReplyKeyboardMarkup([['Показать новую анкету'], ['Сменить сферу'],
#                                                  ['Кандидат подходит']])
#     bot.message.reply_text(text, reply_markup=keyboard_mentor_vibor)


# def mentor_show_anketa(bot, update):
#     # last_user="""{i}""".format(update.user_data)
#     # print(last_user)
#     sfera="""{sphere}""".format(**update.user_data)
#     cursor.execute("""SELECT *
#     FROM mentee
#     WHERE user_sphere=?
#     ORDER BY RANDOM()
#     LIMIT 1""", (sfera, )) #WHERE user_sphere="""{Сфера}""".format(update.user_data')
#     record =cursor.fetchone()
#     for row in record:
#         update.user_data['name']=record[1]
#         update.user_data['sfera'] = record[2]
#         update.user_data['job'] = record[3]
#         update.user_data['motivation'] = record[4]
#         update.user_data['username'] = record[5]
#         update.user_data['i']=record[6]
#     text="""{name}
# @{username}\n
# Сфера: {sfera}
# Должность: {job}
# Мотивация: {motivation}""".format(**update.user_data)
#     keyboard_mentor_vibor = ReplyKeyboardMarkup([['Показать новую анкету'], ['Сменить сферу'],
#                                                   ['Кандидат подходит']])
#     bot.message.reply_text(text, reply_markup=keyboard_mentor_vibor)
#     return "Выбор"