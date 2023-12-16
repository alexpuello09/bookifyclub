import psycopg2

connection = psycopg2.connect(
    host = "localhost",
    user = "postgres",
    database = "bookifyclub",
    password = "Alex9"
)


CREATE_BOOK_TABLE = ("CREATE TABLE IF NOT EXISTS book (book_id SERIAL PRIMARY KEY, title VARCHAR(150), category VARCHAR(150))")
INSERT_INTO_BOOK_TABLE = "INSERT INTO book (title, category) VALUES (%s, %s)"

GET_ALL_THE_BOOKS = ("SELECT * FROM book")