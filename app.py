from flask import Flask, request
import uuid
import data.db as db

app = Flask(__name__)
books = []

#CREATE BOOK
@app.post('/books')
def create_book():
    data = request.get_json() 
    title = data["title"]
    category = data["category"]

    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.CREATE_BOOK_TABLE)
            cursor.execute(db.INSERT_INTO_BOOK_TABLE, (title, category))
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
