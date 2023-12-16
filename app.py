from flask import Flask, request
import uuid
import psycopg2

connection = psycopg2.connect(
    host = "localhost",
    user = "postgres",
    database = "bookifyclub",
    password = "Alex9"
)

app = Flask(__name__)
books = []

CREATE_BOOK_TABLE = ("CREATE TABLE IF NOT EXISTS book (book_id SERIAL PRIMARY KEY, title VARCHAR(150), category VARCHAR(150))")
INSERT_INTO_BOOK_TABLE = "INSERT INTO book (title, category) VALUES (%s, %s)"


#CREATE BOOK
@app.post('/books')
def create_book():
    data = request.get_json() 
    title = data["title"]
    category = data["category"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_BOOK_TABLE)
            cursor.execute(INSERT_INTO_BOOK_TABLE, (title, category))
        return "book created successfully"


#request book
@app.get("/books")
def get_books():
    return books


#Update book
@app.route('/books/<string:id_book>',methods = ['PUT'])
def book_update(id_book):
    datos = request.get_json()
    for book in books:
        if book['id'] == id_book:
            book['name'] = datos['name'],
            book['author'] = datos['author']
            return f" Book with id {id_book} updated successfully"
    return f"Error: Book with id {id_book} not found"

#Delete book
@app.route('/books/<string:id_book>',methods = ['DELETE'])
def book_delete(id_book):
    for book in books:
        if book['id'] == id_book:
            books.remove(book)
            return "Book deleted successfully"
    return "Error: Book with that id not found"
