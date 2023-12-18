import psycopg2

connection = psycopg2.connect(
    host = "localhost",
    user = "postgres",
    database = "bookifyclub",
    password = "Alex9"
)

#BOOK
CREATE_BOOK_TABLE = ("CREATE TABLE IF NOT EXISTS book (book_id SERIAL PRIMARY KEY, title VARCHAR(150), category VARCHAR(150))")
INSERT_INTO_BOOK_TABLE = "INSERT INTO book (title, category) VALUES (%s, %s)"

GET_ALL_THE_BOOKS = ("SELECT * FROM book")
GET_A_BOOK = ("SELECT * FROM book WHERE book_id = (%s)")

UPDATE_BOOK = ("UPDATE book SET title = %s, category = %s WHERE book_id = %s")
DELETE_BOOK = ("DELETE FROM book WHERE book_id = %s")

#=====================================================================================================
#CATEGORY
CREATE_CATEGORY_TABLE = ("CREATE TABLE IF NOT EXISTS category (category_id SERIAL PRIMARY KEY, category_name VARCHAR(150))")
INSERT_INTO_CATEGORY = "INSERT INTO category (category_name) VALUES (%s)"

SELECT_ALL_FROM_CATEGORY = ("SELECT * FROM category")
SELECT_CATEGORY_BY_ID = ("SELECT * FROM category WHERE category_id = (%s)")

UPDATE_CATEGORY = "UPDATE category SET category_name = (%s) WHERE category_id = (%s)"
DELETE_CATEGORY = ("DELETE FROM category WHERE category_id = %s")