CREATE TABLE book (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(30),
    year INTEGER CHECK (year > 0),
    code VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE author (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE room (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER NOT NULL CHECK (number > 0) UNIQUE,
    name VARCHAR(30) NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    current_capacity INTEGER DEFAULT 0
);

CREATE TABLE reader (
    reader_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(12),
    ticket_number VARCHAR(10) NOT NULL UNIQUE,
    room_id INTEGER,
    FOREIGN KEY (room_id) REFERENCES room (room_id) ON DELETE SET NULL
);

CREATE TABLE author_book (
    author_book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    author_id INTEGER,
    FOREIGN KEY (book_id) REFERENCES book (book_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES author (author_id) ON DELETE CASCADE
);

CREATE TABLE book_room (
    book_room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    room_id INTEGER,
    book_count INTEGER CHECK (book_count > 0),
    current_book_count INTEGER DEFAULT book_count,
    FOREIGN KEY (book_id) REFERENCES book (book_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES room (room_id) ON DELETE CASCADE
);

CREATE TABLE reader_book (
    reader_book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reader_id INTEGER,
    book_id INTEGER,
    date DATE,
    FOREIGN KEY (reader_id) REFERENCES reader (reader_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES book (book_id) ON DELETE CASCADE
);

INSERT INTO room(number, name, capacity)
VALUES
(1, "Фантастика", 1),
(2, "Научный", 20),
(3, "Художественная литература", 50),
(4, "Детский", 30);

INSERT INTO author(name)
VALUES
("Стивен Кинг"),
("Достоевский Федор Михайлович"),
("Толстой Лев Николаевич"),
("Замятин Евгений Иванович");

INSERT INTO book(name, year, code)
VALUES
("Мы", 1920, "uye89d726b"),
("Преступление и наказание", 1866, "iuy56akjsh"),
("Братья Карамазовы", 1880, "qw78u1gheo"),
("Война и мир", 1867, "jfur7877ed"),
("Анна Каренина", 1878, "pppp6qh381"),
("Отрочество", 1854, "jstqp7vn92"),
("Оно", 1986, "ytrgmcj142d"),
("Сияние", 1977, "y6wftvn825"),
("Кэрри", 1974, "adufyt9999");

INSERT INTO book_room(book_id, room_id, book_count, current_book_count)
VALUES
(1, 1, 2, 2),
(1, 3, 1, 1),
(2, 3, 2, 2),
(3, 3, 1, 1),
(4, 3, 1, 1),
(5, 3, 1, 1),
(6, 3, 2, 2),
(7, 1, 1, 1),
(8, 1, 1, 1),
(9, 1, 1, 1);

INSERT INTO author_book(book_id, author_id)
VALUES
(1, 4),
(2, 2),
(3, 2),
(4, 3),
(5, 3),
(6, 3),
(7, 1),
(8, 1),
(9, 1);