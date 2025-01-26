import sqlite3
import util


def create_database():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    with open("init.sql", "r", encoding="utf-8") as file:
        cursor.executescript(file.read())

    conn.commit()

    cursor.close()
    conn.close()


def help():
    commands = {
        "/start": "Вывод приветствия",
        "/help": "Информация о командах\n",

        "/add_reader": "Запись нового читателя",
        "/add_book": "Запись (новой) книги в читальный зал",
        "/add_reader_to_room": "Запись читателя в читальный зал\n",

        "/get_readers": "Список всех читателей",
        "/get_books": "Список всех книг",
        "/get_books_by_author": "Список книг автора",
        "/get_book_by_code": "Книга по шифру",
        "/get_rooms": "Список читальных залов\n",

        "/del_reader": "Списывание читателя из библиотеки",
        "/del_book": "Списывание книги",
        "/del_reader_from_room": "Выписка читателя из читального зала\n",

        "/change_book_code": "Изменение шифра книги",
        "/readers_count": "Количество читателей библиотеки",
        "/give_book": "Сдать книгу читателю",
        "/bring_book": "Принять книгу у читателя",
    }
    text = ""
    for command, description in commands.items():
        text += f"{command}: {description}\n"
    return text


def add_reader(name, phone_number, ticket_number):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO reader (name, phone_number, ticket_number)
            VALUES (?, ?, ?)
        ''', (name, phone_number, ticket_number))
    except sqlite3.Error:
        return "Пользователь не добавлен."
        
    conn.commit()

    cursor.close()
    conn.close()

    return "Пользователь успешно добавлен."

def add_book(name, year, code, room_number, book_count, author_name):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    if not util.is_room_number_exist(cursor, room_number):
        return "Такого читального зала нет в базе данных."
    
    if not util.is_author_name_exist(cursor, author_name):
        if not util._add_author_name(cursor, author_name):
            return "ФИО автора не было добавлено в базу данных."
    

    if not util.is_book_name_exist(cursor, name):
        cursor.execute('''
            INSERT INTO book (name, year, code)
            VALUES (?, ?, ?)
        ''', (name, year, code))

        book_id = util._get_book_id_by_book_name(cursor, name)
        author_id = util._get_author_id_by_name(cursor, author_name)

        cursor.execute('''
                   INSERT INTO author_book (book_id, author_id) 
                   VALUES (?, ?)
                   ''', (book_id, author_id))
    
    book_id = util._get_book_id_by_book_name(cursor, name)
    room_id = util._get_room_id_by_number(cursor, room_number)

    cursor.execute('''
                   INSERT INTO book_room (book_id, room_id, book_count, current_book_count) 
                   VALUES (?, ?, ?, ?)
                   ''', (book_id, room_id, book_count, book_count))
        
    conn.commit()

    cursor.close()
    conn.close()

    return "Книга успешно добавлена."

def get_readers():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, phone_number, ticket_number FROM reader")
    readers = cursor.fetchall()

    if readers:
        response = "Список читателей:\n"
        for reader in readers:
            reader_id = util._get_reader_id_by_reader_name(cursor, reader[0])
            response += f"Имя: {reader[0]}, Телефон: {reader[1]}, Номер билета: {reader[2]}, Зал: "
            if util.has_reader_in_room(cursor, reader[0]):
                room_id = util._get_room_id_by_reader_id(cursor, reader_id)
                room_name = util._get_room_name_by_room_id(cursor, room_id)
                response += room_name + "\n"
            else:
                response += "-\n"
            book_ids = util._get_book_id_by_reader_id(cursor, reader_id)
            for book_id in book_ids:
                book_name = util._get_book_name_by_book_id(cursor, book_id)
                s = f"\t\t{book_name}\n"
                response += s
    else:
        response = "В базе данных нет читателей."

    cursor.close()
    conn.close()

    return response

def readers_count():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reader")
    data = cursor.fetchall()
    count = data[0][0]

    response = f"Активных читателей {count}\n"

    cursor.close()
    conn.close()

    return response

def delete_book(name):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    if not util.is_book_name_exist(cursor, name):
        return "Книги с таким именем не существует."
    if util.have_readers_book(cursor, name):
        return "Книгу читают."
    
    book_id = util._get_book_id_by_book_name(cursor, name)
    author_id = util._get_author_id_by_book_id(cursor, book_id)
    room_ids = util._get_room_id_by_book_id(cursor, book_id)
    
    cursor.execute('''
                   DELETE FROM book 
                   WHERE name = ?
                   ''', (name, ))
    cursor.execute('''
                   DELETE FROM author_book 
                   WHERE author_id = ? AND book_id = ?
                   ''', (author_id, book_id))
    for room_id in room_ids:
        cursor.execute('''
                   DELETE FROM book_room 
                   WHERE room_id = ? AND book_id = ?
                   ''', (room_id, book_id))
    conn.commit() 

    cursor.close()
    conn.close()

    return f"Книга '{name}' удалена."


def get_books():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT book.name, year, code, author.name 
                   FROM book 
                   LEFT JOIN author_book USING(book_id)
                   LEFT JOIN author USING(author_id)
                   ''')
    books = cursor.fetchall()

    if books:
        response = "Список книг:\n"
        for book in books:
            response += f"Название: {book[0]}, Год издания: {book[1]}, Шифр: {book[2]}, Автор: {book[3]}\n"
    else:
        response = "В базе данных нет книг."

    cursor.close()
    conn.close()

    return response

def get_books_by_author(author_name):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    if not util.is_author_name_exist(cursor, author_name):
        return "ФИО автора нет в базе данных."

    cursor.execute('''SELECT book.name, year, code, author.name 
                   FROM book 
                   LEFT JOIN author_book USING(book_id)
                   LEFT JOIN author USING(author_id)
                   WHERE author.name = ?
                   ''', (author_name, ))
    books = cursor.fetchall()

    if books:
        response = "Список книг:\n"
        for book in books:
            response += f"Название: {book[0]}, Год издания: {book[1]}, Шифр: {book[2]}, Автор: {book[3]}\n"
    else:
        response = "В базе данных нет книг этого автора."

    cursor.close()
    conn.close()

    return response

def get_book_by_code(code):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    if not util.is_book_code_exist(cursor, code):
        return "Этого шифра книги нет в базе данных."

    cursor.execute('''SELECT book.name, year, code, author.name 
                   FROM book 
                   LEFT JOIN author_book USING(book_id)
                   LEFT JOIN author USING(author_id)
                   WHERE code = ?
                   ''', (code, ))
    books = cursor.fetchall()

    if books:
        response = ""
        for book in books:
            response += f"Название: {book[0]}, Год издания: {book[1]}, Шифр: {book[2]}, Автор: {book[3]}\n"
    else:
        response = "В базе данных нет книг этого автора."

    cursor.close()
    conn.close()

    return response

def change_book_code(code, name):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    if util.is_book_name_exist(cursor, name):
        return "Книги с таким именем не существует."

    cursor.execute('''
                   UPDATE book
                   SET code = ?
                   WHERE name = ?
                   ''', (code, name))
    if cursor.rowcount > 0:
        conn.commit() 

    cursor.close()
    conn.close()

    return f"Код книги '{name}' обновлен на {code}."


def add_reader_to_room(name, room_number):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    if not util.is_room_number_exist(cursor, room_number):
        return "Такого читального зала нет в базе данных."

    if util.is_room_full(cursor, room_number):
        return "Этот читальный зал переполнен."

    if not util.is_reader_name_exist(cursor, name):
        return "Такого читателя нет в базе данных."
    
    if util.has_reader_in_room(cursor, name):
        return "Читатель уже записан в другом читальном зале."
    
    room_id = util._get_room_id_by_number(cursor, room_number)
    
    cursor.execute('''
                    UPDATE reader
                    SET room_id = ?
                    WHERE name = ?
                    ''', (room_id, name))
    cursor.execute('''
                    UPDATE room
                    SET current_capacity = current_capacity + 1
                    WHERE room_id = ?
                    ''', (room_id, ))
    
    conn.commit()

    cursor.close()
    conn.close()

    return "Читатель записан в читальный зал."

def del_reader_from_room(name):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    reader_id = util._get_reader_id_by_reader_name(cursor, name)

    if not util.is_reader_name_exist(cursor, name):
        return "Такого читателя нет в базе данных."
    if util.is_reader_has_books(cursor, reader_id):
        return "У читателя есть не сданные книги."

    room_id = util._get_room_id_by_reader_id(cursor, reader_id)
    
    if not util.has_reader_in_room(cursor, name):
        return "Читатель не прикреплен ни к какому читальному залу."
    
    cursor.execute('''
                    UPDATE reader
                    SET room_id = NULL
                    WHERE name = ?
                    ''', (name, ))
    cursor.execute('''
                    UPDATE room
                    SET current_capacity = current_capacity - 1
                    WHERE room_id = ?
                    ''', (room_id, ))
    
    conn.commit()

    cursor.close()
    conn.close()

    return "Читатель выписан из читального зала."


def get_rooms():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT number, name, capacity, current_capacity FROM room")
    rooms = cursor.fetchall()

    if rooms:
        response = "Список читальных залов:\n"
        for room in rooms:
            room_id = util._get_room_id_by_number(cursor, room[0])
            response += f"{room[0]}; {room[1]}; {room[3]}/{room[2]}\n"
            books = util._get_book_id_by_room_id(cursor, room_id)
            for book in books:
                book_name = util._get_book_name_by_book_id(cursor, book[0])
                s = f"\t{book_name}: {book[2]}/{book[1]}\n"
                response += s
    else:
        response = "В базе данных нет читателей."

    cursor.close()
    conn.close()

    return response

def del_reader(name):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    if not util.is_reader_name_exist(cursor, name):
        return "Такого читателя нет в базе данных."
    reader_id = util._get_reader_id_by_reader_name(cursor, name)
    if util.is_reader_has_books(cursor, reader_id):
        return "У читателя есть не сданные книги."
    if util.has_reader_in_room(cursor, name):
        return "Читатель записан в читальном зале."
    
    del_reader_from_room(name)

    cursor.execute('''
                   DELETE FROM reader 
                   WHERE name = ?
                   ''', (name, ))
    conn.commit() 

    cursor.close()
    conn.close()

    return f"Читатель {name} выписан из библиотеки."

def give_book(book_name, reader_name):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    if not util.is_reader_name_exist(cursor, reader_name):
        return "Такого читателя нет в базе данных."
    if not util.is_book_name_exist(cursor, book_name):
        return "Такой книги нет в базе данных."
    
    if not util.has_reader_in_room(cursor, reader_name):
        return "Читатель не закреплен за читальным залом."
    
    book_id = util._get_book_id_by_book_name(cursor, book_name)
    reader_id = util._get_reader_id_by_reader_name(cursor, reader_name)
    room_id = util._get_room_id_by_reader_id(cursor, reader_id)
    if not util.has_book_in_room(cursor, book_id, room_id):
        return "Данной книги нет в читальном зале, к которому прикреплен читатель."
    if not util.is_book_available_in_room(cursor, book_id, room_id):
        return "Все экземпляры книги заняты."
    
    cursor.execute('''
                   UPDATE book_room
                   SET current_book_count = current_book_count - 1
                   WHERE book_id = ? AND room_id = ?
                   ''', (book_id, room_id))
    cursor.execute('''
                   INSERT INTO reader_book (reader_id, book_id, date)
                   VALUES (?, ?, DATE('now'))
                   ''', (reader_id, book_id))
    conn.commit() 

    cursor.close()
    conn.close()

    return f"Читателю {reader_name} выдана книга {book_name}."

def bring_book(book_name, reader_name):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    if not util.is_reader_name_exist(cursor, reader_name):
        return "Такого читателя нет в базе данных."
    if not util.is_book_name_exist(cursor, book_name):
        return "Такой книги нет в базе данных."
    if not util.has_reader_in_room(cursor, reader_name):
        return "Читатель не закреплен за читальным залом."
    
    book_id = util._get_book_id_by_book_name(cursor, book_name)
    reader_id = util._get_reader_id_by_reader_name(cursor, reader_name)
    room_id = util._get_room_id_by_reader_id(cursor, reader_id)
    if not util.has_book_in_room(cursor, book_id, room_id):
        return "Данной книги нет в читальном зале, к которому прикреплен читатель."
    if not util.is_reader_has_books(cursor, reader_id):
        return "За читателем нет записанных книг"
    if not util.is_reader_has_book(cursor, reader_id, book_id):
        return "Данная книга не записана за читателем"
    
    cursor.execute('''
                   UPDATE book_room
                   SET current_book_count = current_book_count + 1
                   WHERE book_id = ? AND room_id = ?
                   ''', (book_id, room_id))
    cursor.execute('''
                   DELETE FROM reader_book 
                   WHERE reader_id = ? AND book_id = ?
                   ''', (reader_id, book_id))
    conn.commit() 

    cursor.close()
    conn.close()

    return f"Книга {book_name} читателя {reader_name} сдана."