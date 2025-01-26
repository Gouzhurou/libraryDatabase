import sqlite3

def is_reader_name_exist(cursor, name) -> bool:
    cursor.execute('''
                   SELECT name
                   FROM reader
                   ''')
    
    readers = cursor.fetchall()
    reader_names = []
    for reader in readers:
        reader_names.append(reader[0])

    if name not in reader_names:
        return False
    
    return True

def is_room_number_exist(cursor, number) -> bool:
    cursor.execute('''
                   SELECT number
                   FROM room
                   ''')
    
    rooms = cursor.fetchall()
    room_numbers = []
    for room in rooms:
        room_numbers.append(room[0])

    if number.isdigit() and int(number) not in room_numbers:
        return False
    
    return True

def is_book_name_exist(cursor, name) -> bool:
    cursor.execute('''
                   SELECT name
                   FROM book
                   ''')
    
    books = cursor.fetchall()
    book_names = []
    for book in books:
        book_names.append(book[0])

    if name not in book_names:
        return False
    
    return True

def is_author_name_exist(cursor, name) -> bool:
    cursor.execute('''
                   SELECT name
                   FROM author
                   ''')
    
    authors = cursor.fetchall()
    author_names = []
    for author in authors:
        author_names.append(author[0])

    if name not in author_names:
        return False
    
    return True

def is_book_code_exist(cursor, book_code):
    cursor.execute('''
                   SELECT code
                   FROM book
                   ''')
    
    data = cursor.fetchall()
    codes = []
    for code in data:
        codes.append(code[0])

    if book_code not in codes:
        return False
    
    return True

def is_room_full(cursor, number):
    cursor.execute('''
                   SELECT capacity, current_capacity
                   FROM room
                   WHERE number = ?
                   ''', (number, ))
    
    data = cursor.fetchall()
    capacity = data[0][0]
    current_capacity = data[0][1]

    if current_capacity == capacity:
        return True
    
    return False

def have_readers_book(cursor, name):
    cursor.execute('''
                   SELECT *
                   FROM book
                   INNER JOIN reader_book USING(book_id)
                   WHERE name = ?
                   ''', (name, ))
    data = cursor.fetchall()
    if len(data) > 0:
        return True
    
    return False


def is_reader_has_books(cursor, reader_id):
    cursor.execute('''
                   SELECT book_id
                   FROM reader_book
                   WHERE reader_id = ?
                   ''', (reader_id, ))
    data = cursor.fetchall()
    if len(data) > 0:
        return True
    
    return False

def has_reader_in_room(cursor, name):
    cursor.execute('''
                   SELECT room_id
                   FROM reader
                   WHERE name = ?
                   ''', (name, ))
    
    data = cursor.fetchall()
    room_id = data[0][0]

    if room_id is not None:
        return True
    
    return False

def has_book_in_room(cursor, book_id, room_id):
    cursor.execute('''
                   SELECT book_id
                   FROM book_room
                   WHERE room_id = ?
                   ''', (room_id, ))
    
    data = cursor.fetchall()
    book_ids = []
    for d in data:
        book_ids.append(d[0])

    if book_id not in book_ids:
        return False
    
    return True

def is_book_available_in_room(cursor, book_id, room_id):
    cursor.execute('''
                   SELECT current_book_count
                   FROM book_room
                   WHERE room_id = ? AND book_id = ?
                   ''', (room_id, book_id))
    
    data = cursor.fetchall()
    current_book_count = data[0][0]

    if current_book_count > 0:
        return True
    
    return False

def is_reader_has_book(cursor, reader_id, book_id):
    cursor.execute('''
                   SELECT COUNT(*)
                   FROM reader_book
                   WHERE reader_id = ? AND book_id = ?
                   ''', (reader_id, book_id))
    
    data = cursor.fetchall()

    if data[0][0] > 0:
        return True
    
    return False

def _get_author_id_by_book_id(cursor, book_id):
    cursor.execute('''
                   SELECT author_id
                   FROM author_book
                   WHERE book_id = ?
                   ''', (book_id, ))
    data = cursor.fetchall()
    author_id = data[0][0]
    return author_id

def _get_room_id_by_book_id(cursor, book_id):
    cursor.execute('''
                   SELECT room_id
                   FROM book_room
                   WHERE book_id = ?
                   ''', (book_id, ))
    data = cursor.fetchall()
    room_ids = []
    for d in data:
        room_ids.append(d[0])
    return room_ids

def _get_room_id_by_reader_id(cursor, reader_id):
    cursor.execute('''
                   SELECT room_id
                   FROM reader
                   WHERE reader_id = ?
                   ''', (reader_id, ))
    data = cursor.fetchall()
    room_id = data[0][0]
    return room_id

def _get_room_name_by_room_id(cursor, room_id):
    cursor.execute('''
                   SELECT name
                   FROM room
                   WHERE room_id = ?
                   ''', (room_id, ))
    data = cursor.fetchall()
    name = data[0][0]
    return name

def _get_reader_id_by_reader_name(cursor, name):
    cursor.execute('''
                   SELECT reader_id
                   FROM reader
                   WHERE name = ?
                   ''', (name, ))
    data = cursor.fetchall()
    reader_id = data[0][0]
    return reader_id

def _get_book_id_by_book_name(cursor, name):
    cursor.execute('''
                   SELECT book_id
                   FROM book
                   WHERE name = ?
                   ''', (name, ))
    data = cursor.fetchall()
    book_id = data[0][0]
    return book_id

def _get_book_name_by_book_id(cursor, book_id):
    cursor.execute('''
                   SELECT name
                   FROM book
                   WHERE book_id = ?
                   ''', (book_id, ))
    data = cursor.fetchall()
    if len(data) > 0:
        name = data[0][0]
        return name
    return None

def _add_author_name(cursor, name):
    try:
        cursor.execute('''
            INSERT INTO author (name)
            VALUES (?)
        ''', (name, ))
    except sqlite3.Error: 
        return False
    
    return True

def _get_author_id_by_name(cursor, name):
    cursor.execute('''
                   SELECT author_id
                   FROM author
                   WHERE name = ?
                   ''', (name, ))
    data = cursor.fetchall()
    author_id = data[0][0]
    return author_id

def _get_room_id_by_number(cursor, number):
    cursor.execute('''
                   SELECT room_id
                   FROM room
                   WHERE number = ?
                   ''', (number, ))
    data = cursor.fetchall()
    room_id = data[0][0]
    return room_id

def _get_book_id_by_reader_id(cursor, reader_id):
    cursor.execute('''
                   SELECT book_id
                   FROM reader_book
                   WHERE reader_id = ?
                   ''', (reader_id, ))
    data = cursor.fetchall()
    book_ids = []
    for d in data:
        book_ids.append(d[0])
    return book_ids

def _get_book_id_by_room_id(cursor, room_id):
    cursor.execute('''
                   SELECT book_id, book_count, current_book_count
                   FROM book_room
                   WHERE room_id = ?
                   ''', (room_id, ))
    data = cursor.fetchall()
    return data