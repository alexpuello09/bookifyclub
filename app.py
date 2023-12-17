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


#GET ALL THE BOOKS CONTENT
@app.get("/books")
def get_books():
    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.GET_ALL_THE_BOOKS)
            result = cursor.fetchall()
        return result
        

#GET A BOOK BY ITS ID
@app.get("/books/<int:id>")
def get_book(id):
    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.GET_A_BOOK, (id,))
            result = cursor.fetchone()

            if result is not None:
                return list(result)
            else:
                return f"Error: Book with id {id} not found", 404
    
#UPDATE A BOOK
@app.put("/books/<int:id_book>")
def book_update(id_book):
    data = request.get_json()
    title = data["title"]
    category = data["category"]

    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.UPDATE_BOOK, (title, category, id_book))

            if cursor.rowcount > 0:
                return f"Book with id {id_book} updated successfully"
            else:
                return (f"Error: Book with id {id_book} not found"), 404

#Delete book
@app.delete('/books/<int:id_book>')
def book_delete(id_book):
    with db.connection:
        with db.connection.cursor() as cursor: 
            cursor.execute(db.DELETE_BOOK, (id_book,))

            if cursor.rowcount > 0:
                return "book deleted successfully"
            else:
                return (f"Book with id {id_book} not found"), 404
