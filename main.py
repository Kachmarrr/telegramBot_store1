import os

import sqlite3

import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot('6711585462:AAHGNVfsih00YbwOCoenpv8PMWgdJpMc2Zg')

#як тількb користувач натискає команду start він можен оюрати між "🔥Навчання" i "😎Корисне"
#тут описується привітання до користувача та вибір який він може зробити
@bot.message_handler(commands=['start'])
def start(message):
    # Підключаємося до бази даних
    conn = sqlite3.connect('metsource.db')
    cur = conn.cursor()

    # Створюємо таблицю, якщо її не існує
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), password VARCHAR(50))')
    conn.commit()

    # Закриваємо з'єднання з базою даних
    cur.close()
    conn.close()

    # Викликаємо функцію, що запитує ім'я користувача
    ask_for_name(message)


def ask_for_name(message):
    bot.send_message(message.chat.id, "Привіт! Як тебе звати?")
    bot.register_next_step_handler(message, save_name)


def save_name(message):
    name = message.text
    save_user_to_db(message.chat.id, name)
    send_welcome_message(message)


def save_user_to_db(user_id, name):
    # Підключаємося до бази даних
    conn = sqlite3.connect('metsource.db')
    cur = conn.cursor()

    # Вставляємо дані користувача в таблицю
    cur.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()

    # Закриваємо з'єднання з базою даних
    cur.close()
    conn.close()


def send_welcome_message(message):
    # Створюємо клавіатуру з двома кнопками
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🔥Навчання', callback_data='navchannya'))
    markup.add(types.InlineKeyboardButton('😎Корисне', callback_data='korisne'))

    # Відправляємо привітальне повідомлення
    welcome_message = '''*Ласкаво просимо!*

    "Навчання" містить розділи "Курси" та "Книги", які постійно поповнюються актуальними матеріалами для навчання та підвищення кваліфікації.

    "Корисне" - збірка топових ресурсів, якими слід користуватися.

    Удачі, твоя команда *metSource!*'''
    welcome_message_highlighted = welcome_message.replace('Навчання', '*Навчання*').replace('Курси', '*Курси*').replace(
        'Книги', '*Книги*').replace('Корисне', '*Корисне*')
    bot.send_message(message.chat.id, welcome_message_highlighted, parse_mode='Markdown', reply_markup=markup)

# Обробник для кнопки "🔥Навчання"
# користувач обирає між кнопками, також тут відбувається сортування двох кнопок "💌Курси" та "📚Книги", і при бажанні він може повернутися назад
@bot.callback_query_handler(func=lambda call: call.data == 'navchannya')
def navchannya_handler(call):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('⚡🌩Новачкам', callback_data='novachkam'))
    markup.row(types.InlineKeyboardButton('✅Завдання', callback_data='task'))
    markup.row(types.InlineKeyboardButton('💌Курси', callback_data='kyrs'), types.InlineKeyboardButton('📚Книги', callback_data='books'))
    markup.add(types.InlineKeyboardButton('⬅️ Назад', callback_data='back_to_main'))
    bot.send_message(call.message.chat.id, "Оберіть розділ навчання:", reply_markup=markup)


#обробник кнопки навчання(task)
@bot.callback_query_handler(func=lambda call: call.data == 'task')
def task_callback(call):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('завдання з OOP', callback_data='task1'))
    bot.send_message(call.message.chat.id, "завдання можна використовувати не тільки для одної мови: ", reply_markup=markup)

#обробник кнопки завдання(task)
import os

@bot.callback_query_handler(func=lambda call: call.data == 'task1')
def task_callback(call):
    if call.data == 'task1':
        directory = './media/practiceOOP/'
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    bot.send_document(call.message.chat.id, file)



    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            bot.send_document(call.message.chat.id, file)
    else:
        bot.send_message(call.message.chat.id, "Файл не знайдено")



#обробник кнопки новачкам
@bot.callback_query_handler(func=lambda call: call.data == 'novachkam')
def novchkam_callback(call):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('рекомендації автора', callback_data='fromAuthor'))
    markup.row(types.InlineKeyboardButton('java', callback_data='javastart'), types.InlineKeyboardButton('python', callback_data='pythonstart'))
    bot.send_message(call.message.chat.id, "якщо ти тільки починаєш тоді можеш переглянути рекомендації автора: ", reply_markup=markup)

#обробка кнопок для новачків(від автора та початок роботи)
@bot.callback_query_handler(func=lambda call: call.data in ['fromAuthor', 'javastart', 'pythonstart'])
def startTOnewbie_callback(call):
    if call.data == 'fromAuthor':
        answer = ''
    elif call.data == 'javastart':
        answer = ''

    bot.send_message(call.message.chat.id, answer)

#Обробник для кнопки "😎Корисне"
@bot.callback_query_handler(func=lambda call: call.data == 'korisne')
def korisne_handler(call):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('java', callback_data='java100'), types.InlineKeyboardButton('python', callback_data='python100'))
    markup.row(types.InlineKeyboardButton('javascript', callback_data='javascript100'), types.InlineKeyboardButton('C#/.NET', callback_data='C#100'))
    bot.send_message(call.message.chat.id, "цей розділ більше зроблений для мотивації, тому тут я залишу які питання потрібно знати на рівень junior developer з таких мов: ", reply_markup=markup)

#обробник кнопок java100 and python100
@bot.callback_query_handler(func=lambda call: call.data in ['java100', 'python100', 'javascript100', 'C#100'])
def question100_handler(call):
    if call.data == 'java100':
        question_url = 'https://dou.ua/lenta/articles/interview-questions-java-developer/?from=tiles'
    elif call.data == 'python100':
        question_url = 'https://dou.ua/lenta/articles/interview-questions-python-developer/'
    elif call.data == 'javascript100':
        question_url = 'https://dou.ua/lenta/articles/interview-questions-javascript-developer/'
    elif call.data == 'C#100':
        question_url = 'https://dou.ua/lenta/articles/interview-questions-net-developer/'

    bot.send_message(call.message.chat.id, question_url)


# Обробник для кнопки "💌Курси" та з якою мовою програмування книги будуть повязані
@bot.callback_query_handler(func=lambda call: call.data == 'kyrs')
def kyrs_handler(call):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('HTML', callback_data='html_kyrs'))
    markup.row(types.InlineKeyboardButton('Java', callback_data='java_kyrs'), types.InlineKeyboardButton('python', callback_data='python_kyrs'))
    markup.row(types.InlineKeyboardButton('javascript', callback_data='javascript_kyrs'))
    bot.send_message(call.message.chat.id, "Оберіть мову програмування:", reply_markup=markup)

#обробник кнопки курси по пайтон
@bot.callback_query_handler(func=lambda call: call.data == 'python_kyrs')
def python_kyrs_handler(call):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('', callback_data='python_kyrs'))
    bot.send_message(call.message.chat.id, "всі курси які є по python на даний момент", reply_markup=markup)

#обробка для callback=python_kyrs
@bot.callback_query_handler(func=lambda call: call.data == 'python_kyrs')
def python_kyrs_handler(call):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(''))



#обробник кнопки курсів по HTML
@bot.callback_query_handler(func=lambda call: call.data == 'html_kyrs')
def html_kyrs_handler(call):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('великий ПЛАТНИЙ курс по HTML з домашнім завданням', callback_data='html_bigList'))
    bot.send_message(call.message.chat.id, "Курси по html:", reply_markup=markup)

#кнопки до курсу по Html
@bot.callback_query_handler(func=lambda call: call.data == 'html_bigList')
def send_html_kyrs(call):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Лекція 1', callback_data='html_bigList_lecture_1'))
    markup.row(types.InlineKeyboardButton('Лекція 2 з дз', callback_data='html_bigList_lecture_HW_2'))
    markup.row(types.InlineKeyboardButton('лекція 3-4 ', callback_data='html_bigList_lecture_3-4'))
    markup.row(types.InlineKeyboardButton('Лекція 5', callback_data='html_bigList_lecture_5'))
    markup.row(types.InlineKeyboardButton('Лекція 6', callback_data='html_bigList_lecture_6'))
    markup.row(types.InlineKeyboardButton('Лекція 7', callback_data='html_bigList_lecture_7'))
    markup.row(types.InlineKeyboardButton('дз 8-9', callback_data='html_bigList_8-9_HW'))
    markup.row(types.InlineKeyboardButton('Додаткові завдання', callback_data='html_bigList_tasks'))
    bot.send_message(call.message.chat.id, "курс по HTML: :", reply_markup=markup)

# оюробник кнопок курсу по html(лекції, дз тощо...)
@bot.callback_query_handler(func=lambda call: call.data in ['html_bigList_lecture_1', 'html_bigList_lecture_HW_2', 'html_bigList_lecture_3-4', 'html_bigList_lecture_5',
                                                            'html_bigList_lecture_6', 'html_bigList_lecture_7', 'html_bigList_8-9_HW', 'html_bigList_tasks'])
def send_html(call):
    if call.data == 'html_bigList_lecture_1':
        lecture = 'Лекція 1 : https://vimeo.com/760431927/72f1dd18da ДЗ в описі'
    elif call.data == 'html_bigList_lecture_HW_2':
        lecture = 'https://vimeo.com/761572005/4b0dc5a1d7 - Лекція 2 та ДЗ'
    elif call.data == 'html_bigList_lecture_3-4':
        lecture = 'Лекція 3-4 : https://vimeo.com/765248884/0a0c6565b4'
    elif call.data == 'html_bigList_lecture_5':
        lecture = 'Лекція 5 : https://vimeo.com/766216973/b04caf8daf'
    elif call.data == 'html_bigList_lecture_6':
        lecture = 'Лекція 6 : https://drive.google.com/drive/folders/16zF1ZiY1dAvcdKwCHjW0DRuWGuweAC6C?usp=share_link'
    elif call.data == 'html_bigList_lecture_7':
        lecture = '''Лекція 7 : https://vimeo.com/777673618/e9f5eb8c0f
ДЗ 
https://www.figma.com/file/djwqJH8abh8k9eM3n0P7Fi/ITEA-7-8?node-id=0%3A1
Проєкт має складатись з 4-х екранів.
Хедер має бути прикріплений до верху сторінки як це вказано на макеті  та спускатись в слід за скроллом  користувача. 
Сторінка Gallery 
До центру з лівої та правої сторони виїжджають по 2 картинки за першу секунду та бокові картинки з ліва та права додаються на другій секунді. Знадобиться анімація та трансформація транслейт  
сторінка Services
Картинки з кружечками мають крутитись одна за одною по часовій стрілці міняючись місцями (постійно анімуються, але не швидко, наприклад одна анімація триває 5секунд)
сторінка Team
При наведених на карточки має підсвічуватись ім'я працівника як на макеті. (див. макет)
Сторінка Contact Us
Сторінка контактів. Враховуйте всі посилання вони мають бути робочими та вбудуйте карту з google map


timing function https://cubic-bezier.com/#.17,.67,.83,.67
перевірка властивостей для підтримки браузерами
 https://caniuse.com/
 https://html5test.com/'''
    elif call.data == 'html_bigList_8-9_HW':
        lecture = '''ДЗ 8-9.5 

Запис : https://vimeo.com/780883546/e965242d18

Макет 
https://www.figma.com/file/Y0E9LZXMqHmN9gmqN8qcfH/hw-lesson-7-8-(Copy)?node-id=0%3A1&t=lqDIFZZ3OXG4JuiZ-0
Адаптивність. 

Використовувати семантичну, адаптивну, респонсивну (гумову) верстку, валідну 
Розширення < 768px
Gallery
Кожна картинка починається з нової строки з'являються одна з лівої  друга з правої сторони і т.д 
Services
Залишаємо анімацію кружків з тестом та прибираємо картинку перукаря 
Team
Кожна картинка починається з нової строки при натиску на зображення плавно з'являється ім'я члена команди 
Contact Us
Першою показується карта потім форма 

Розширення < 992px
Gallery
Робимо 3 рядки по 2 картинки ліві картинки виїжджають з лівої сторони, а праві з правої.
Services
картинку перукаря робимо першою та з нової строки
Залишаємо анімацію кружків з тестом
Team
2 співробітники на одній строці при наведені на зображення плавно з'являється ім'я члена команди 
Contact Us
Першою показується Форма потім мапа 

Розширення > 992px
Все як на макеті, але якщо розширення буде більшим ніж 1620px, то мають бути бокові відступи.'''
    elif call.data == 'html_bigList_tasks':
        lecture = '''Ось тут додаткові задачки зібрав одним повідомленням
        Додаткове ДЗ Верстка 

        https://www.figma.com/file/r73iFSdplSF9TsCYTyjSXy/prog-dop?node-id=0%3A1&t=83ynyGRC6N9V2kek

        Ось макет. Тут десктоп та мобільна верстка 
        - Мобільна до 768 пікселів 
        - Десктоп до 1600 пікселів

        Додатково Таблиці 

        По табличкам якщо цікаво можете створити такий сайт : https://www.figma.com/file/Z1JE3jWbktx3pFJmqIRWEg/HW-2-video-%F0%9F%94%BA?t=83ynyGRC6N9V2kek-0


        ⚠️
        - Умова, при наведені на елемент періодичної таблиці, анімуйте елемент. Збільшити, наприклад.
        - Використовуйте методологію БЕМ - https://ru.bem.info/methodology/key-concepts/'''

    bot.send_message(call.message.chat.id, lecture)

#Обробник для кнопки "📚Книги" та з якою мовою програмування книги будуть повязані
@bot.callback_query_handler(func=lambda call: call.data == 'books')
def books_handler(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Java', callback_data='java_books'))
    markup.add(types.InlineKeyboardButton('Python', callback_data='python_books'))
    markup.add(types.InlineKeyboardButton('JavaScript', callback_data='javascript_books'))
    bot.send_message(call.message.chat.id, "Оберіть мову програмування:", reply_markup=markup)


# Обробник для кнопки "Java" книжки по джава
@bot.callback_query_handler(func=lambda call: call.data == 'java_books')
def java_books_handler(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Head First Java', callback_data='head_first_java'))
    markup.add(types.InlineKeyboardButton('Filosofia_java', callback_data='filosofia_java'))
    markup.add(types.InlineKeyboardButton('Joshua Bloch - Effective Java (3rd) - 2018', callback_data='effective_java'))
    markup.add(types.InlineKeyboardButton('izuchaem_java_mirovoy(на російській)', callback_data = 'izuchaem_java_mirovoy'))
    bot.send_message(call.message.chat.id, "Оберіть книгу:", reply_markup=markup)


# Обробник для книжок по java та надсилання залежно від вибору користувача
@bot.callback_query_handler(func=lambda call: call.data in ['head_first_java', 'filosofia_java', 'effective_java', 'izuchaem_java_mirovoy'])
def send_java_book(call):
    if call.data == 'head_first_java':
        file_path = './media/Head_First_Java_Second_Edition.pdf'
    elif call.data == 'filosofia_java':
        file_path = './media/Filosofia_Java.pdf'
    elif call.data == 'effective_java':
        file_path = './media/Joshua Bloch - Effective Java (3rd) - 2018.pdf'
    elif call.data == 'izuchaem_java_mirovoy':
        file_path = './media/k_syerra_b_beyts_-_izuchaem_java_mirovoy_kom.pdf'

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            bot.send_document(call.message.chat.id, file)
    else:
        bot.send_message(call.message.chat.id, "Файл не знайдено")

# ті кнопки обробників яких ще немає
@bot.callback_query_handler(func=lambda call: call.data in ['novachkam', 'kyrs', 'recent_books', 'python_books', 'korisne'])
def additional_navchannya_handler(call):
    bot.send_message(call.message.chat.id, f"Ви обрали {call.data}")

# Якщо користувач ввів незрозумілу команду
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я не розумію цієї команди. Використовуйте /start для початку.")

bot.polling(none_stop=True)