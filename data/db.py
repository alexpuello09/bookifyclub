import psycopg2
import os

data_password = os.environ.get('DB_PASSWORD_FILE')
with open(data_password, 'r') as password:
    dbpassword = password.read()

data_host = os.environ.get('DB_HOST_FILE')
with open(data_host, 'r') as host:
     dbhost = host.read()

data_name = os.environ.get('DB_NAME_FILE')
with open(data_name, 'r') as name:
    dbname = name.read()

data_user = os.environ.get('DB_USER_FILE')
with open(data_user, 'r') as user:
    dbuser = user.read()

connection = psycopg2.connect(
    host = dbhost,
    port = 5432,
    user = dbuser,
    database = dbname,
    password = dbpassword
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

#USER
#=====================================================================================================

CREATE_USER = ("CREATE TABLE IF NOT EXISTS user_account (name VARCHAR(100), lastname VARCHAR(100), username VARCHAR(100), email VARCHAR(100), password VARCHAR(15), created_at TIMESTAMP, update_at TIMESTAMP, token VARCHAR(350), PRIMARY KEY (username, email))")
INSER_INTO_USER = ("INSERT INTO user_account (name,  lastname, username, email, password , created_at, token) VALUES (%s, %s, %s, %s, %s, %s, %s)")

GET_ALL_USER = ("SELECT * FROM user_account")
GET_A_USER = ("SELECT * FROM user_account WHERE token = %s")

UPDATE_USER = ("UPDATE user_account SET password = (%s), update_at = (%s) WHERE token = (%s) AND password = (%s) AND username = (%s);")
DELETE_USER = ("DELETE FROM user_account WHERE token = (%s)")
