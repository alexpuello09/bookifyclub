import os
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import sqlalchemy

connection_pool=None

def init_database():
    global connection_pool
    instance_connection_name = os.environ.get('INSTANCE_CONNECTION_NAME')
    db_pass = os.environ.get('DB_PASS')
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
    connector = Connector()

    connection_creator = lambda :connector.connect(
        instance_connection_name,
        "pg8000",
        user=db_user,
        password=db_pass,
        db=db_name,
        ip_type=ip_type
        )

    connection_pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=connection_creator)




#BOOK

CREATE_BOOK_TABLE = sqlalchemy.text(
"CREATE TABLE IF NOT EXISTS book (book_id SERIAL PRIMARY KEY, title VARCHAR(150), category VARCHAR(150))"
)


INSERT_INTO_BOOK_TABLE = sqlalchemy.text(
    "INSERT INTO book (title, category) VALUES (:title, :category)"
)

GET_ALL_THE_BOOKS = sqlalchemy.text(
    "SELECT * FROM book"
    )
    
GET_A_BOOK = sqlalchemy.text(
    "SELECT * FROM book WHERE book_id = :book_id"
)

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
