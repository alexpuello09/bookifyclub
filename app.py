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

#request book
@app.get("/books")
def get_books():
    return books

#Create book
@app.post('/books')
def create_book():
    data = request.get_json()
    id = str(uuid.uuid4())
    new_book =  {
        'id': id,
        'name': data["name"],
        'author': data["author"]
    }
    books.append(new_book)
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
