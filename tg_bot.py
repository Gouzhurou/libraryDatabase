import telebot
import db

with open('token/token.txt', 'r') as file:
    TOKEN = file.read()
bot = telebot.TeleBot(TOKEN)
db.create_database()


@bot.message_handler(commands=["start"])
def cmd_start(message):
    text = "Привет! Это Бот, который тебе поможет управлять библиотекой.\n\n"
    text += db.help()
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["help"])
def cmd_help(message):
    text = db.help()
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["add_reader"])
def cmd_add_reader(message):
    bot.send_message(message.chat.id, "Введите имя читателя:")
    bot.register_next_step_handler(message, input_reader_name, is_add_reader=True)


@bot.message_handler(commands=["del_reader"])
def cmd_del_reader(message):
    bot.send_message(message.chat.id, "Введите имя читателя:")
    bot.register_next_step_handler(message, input_reader_name, is_del_reader=True)


@bot.message_handler(commands=["add_book"])
def cmd_add_book(message):
    bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(message, input_book_name, is_add_book=True)


@bot.message_handler(commands=["del_book"])
def cmd_del_book(message):
    bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(message, input_book_name, is_del_book=True)


@bot.message_handler(commands=["add_reader_to_room"])
def cmd_add_reader_to_room(message):
    bot.send_message(message.chat.id, "Введите имя читателя:")
    bot.register_next_step_handler(message, input_reader_name, is_add_reader_to_room=True)


@bot.message_handler(commands=["del_reader_from_room"])
def cmd_del_reader_from_room(message):
    bot.send_message(message.chat.id, "Введите имя читателя:")
    bot.register_next_step_handler(message, input_reader_name, is_del_reader_from_room=True)


@bot.message_handler(commands=["get_readers"])
def cmd_get_readers(message):
    response = db.get_readers()
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=["readers_count"])
def cmd_readers_count(message):
    response = db.readers_count()
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=["get_rooms"])
def cmd_get_rooms(message):
    response = db.get_rooms()
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=["change_book_code"])
def cmd_change_book_code(message):
    bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(message, input_book_name, is_change_book_code=True)


@bot.message_handler(commands=["get_books"])
def cmd_get_books(message):
    response = db.get_books()
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=["get_books_by_author"])
def cmd_get_books_by_author(message):
    bot.send_message(message.chat.id, "Введите ФИО автора:")
    bot.register_next_step_handler(message, input_author_name, is_get_books_by_author=True)


@bot.message_handler(commands=["get_book_by_code"])
def cmd_get_book_by_code(message):
    bot.send_message(message.chat.id, "Введите шифр книги:")
    bot.register_next_step_handler(message, input_book_code, is_get_book_by_code=True)


@bot.message_handler(commands=["give_book"])
def cmd_give_book(message):
    bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(message, input_book_name, is_give_book=True)


@bot.message_handler(commands=["bring_book"])
def cmd_bring_book(message):
    bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(message, input_book_name, is_bring_book=True)


def input_reader_name(
        message, 
        is_add_reader=False, 
        is_add_reader_to_room=False, 
        is_del_reader_from_room=False,
        is_del_reader=False,
        is_give_book=False,
        is_bring_book=False,
        book_name=None):
    name = message.text
    if is_bring_book:
        response = db.bring_book(book_name, name)
        bot.send_message(message.chat.id, response)
    if is_give_book:
        response =  db.give_book(book_name, name)
        bot.send_message(message.chat.id, response)
    if is_del_reader:
        response =  db.del_reader(name)
        bot.send_message(message.chat.id, response)
    if is_add_reader:
        bot.send_message(message.chat.id, "Введите номер телефона (8 или +7 в начале и 10 цифр номера телефона):")
        bot.register_next_step_handler(message, input_phone_number, name)
    if is_add_reader_to_room:
        bot.send_message(message.chat.id, "Введите номер читального зала:")
        bot.register_next_step_handler(message, input_room_number, name, is_add_reader_to_room=True)
    if is_del_reader_from_room:
        response =  db.del_reader_from_room(name)
        bot.send_message(message.chat.id, response)

def input_phone_number(message, name):
    phone_number = message.text
    bot.send_message(message.chat.id, "Введите номер читательского билета:")
    bot.register_next_step_handler(message, input_ticket_number, name, phone_number)

def input_ticket_number(message, name, phone_number):
    ticket_number = message.text
    response = db.add_reader(name, phone_number, ticket_number)  
    bot.send_message(message.chat.id, response)

def input_room_number(
        message, 
        name,
        year=None,
        code=None,
        is_add_book=False,
        is_add_reader_to_room=False):
    room_number = message.text
    if is_add_reader_to_room:
        response = db.add_reader_to_room(name, room_number)
        bot.send_message(message.chat.id, response)
    if is_add_book:
        bot.send_message(message.chat.id, "Введите количество книг:")
        bot.register_next_step_handler(message, input_book_count, name, year, code, room_number, is_add_book=True)

def input_book_count(
        message,
        name,
        year,
        code,
        room_number,
        is_add_book=False):
    book_count = message.text
    if is_add_book:
        bot.send_message(message.chat.id, "Введите ФИО автора:")
        bot.register_next_step_handler(message, input_author_name, name, year, code, room_number, book_count, is_add_book=True)

def input_author_name(
    message,
    book_name=None,
    year=None,
    code=None,
    room_number=None,
    book_count=None,
    is_add_book=False,
    is_get_books_by_author=False):
    author_name = message.text
    if is_add_book:
        response = db.add_book(book_name, year, code, room_number, book_count, author_name)
        bot.send_message(message.chat.id, response)
    if is_get_books_by_author:
        response = db.get_books_by_author(author_name)
        bot.send_message(message.chat.id, response)

def input_book_name(
        message, 
        is_del_book=False, 
        is_change_book_code=False, 
        is_add_book=False,
        is_give_book=False,
        is_bring_book=False,
        code=None):
    name = message.text
    if is_bring_book:
        bot.send_message(message.chat.id, "Введите имя читателя:")
        bot.register_next_step_handler(message, input_reader_name, book_name=name, is_bring_book=True)
    if is_give_book:
        bot.send_message(message.chat.id, "Введите имя читателя:")
        bot.register_next_step_handler(message, input_reader_name, book_name=name, is_give_book=True)
    if is_add_book:
        bot.send_message(message.chat.id, "Введите год издания книги:")
        bot.register_next_step_handler(message, input_book_year, name, is_add_book=True)
    if is_del_book:
        response = db.delete_book(name)
        bot.send_message(message.chat.id, response)
    if is_change_book_code and code is None:
        bot.send_message(message.chat.id, "Введите новый шифр книги:")
        bot.register_next_step_handler(message, input_book_code, name, is_change_book_code=True)

def input_book_code(
        message, 
        name=None, 
        year=None,
        is_change_book_code=False,
        is_add_book=False,
        is_get_book_by_code=False):
    code = message.text
    if is_change_book_code:
        response = db.change_book_code(code, name)
        bot.send_message(message.chat.id, response)
    if is_add_book:
        bot.send_message(message.chat.id, "Введите номер читального зала:")
        bot.register_next_step_handler(message, input_room_number, name, year, code, is_add_book=True)
    if is_get_book_by_code:
        response = db.get_book_by_code(code)
        bot.send_message(message.chat.id, response)

def input_book_year(
        message, 
        name,
        is_add_book=False):
    year = message.text
    if is_add_book:
        bot.send_message(message.chat.id, "Введите шифр книги:")
        bot.register_next_step_handler(message, input_book_code, name, year, is_add_book=True)

bot.polling(none_stop=True)
