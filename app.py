from flask import Flask, request
app = Flask(__name__)
books = [
    {
        "id": 1,
        "name": "Cien años de soledad",
        "author": "Gabriel García Márquez"
    }
]

#request book
@app.get("/books")
def get_books():
    return books

#Create book
@app.post('/books')
def create_book():
    data = request.get_json()
    new_book =  {
        'id': len(books) +1,
        'name': data["name"],
        'author': data["author"]
    }
    books.append(new_book)
    return books

#Update book
@app.route('/books/<int:id_book>',methods = ['PUT'])
def book_update(id_book):
    datos = request.get_json()
    for book in books:
        if book['id'] == id_book:
            book['name'] = datos['name'],
            book['author'] = datos['author']
            return book
    return "Error: Book with that id not found"

#Delete book
@app.route('/books/<int:id_book>',methods = ['DELETE'])
def book_delete(id_book):
    for book in books:
        if book['id'] == id_book:
            books.remove(book)
            return "Book deleted successfully"
    return "Error: Book with that id not found"
