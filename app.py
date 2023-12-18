from flask import Flask, request
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
    
            books_dict = []
            for book in result:
                books_dict.append({"id":book[0], "title": book[1], "category":book[2]})
            return books_dict

        
#GET A BOOK BY ITS ID
@app.get("/books/<int:id>")
def get_book(id):
    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.GET_A_BOOK, (id,))
            result = cursor.fetchone()

            if result is not None:
                result_json = {"id": result[0], "title": result[1], "category": result[2]}
                return (result_json)
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
                return (f"Error 404: Book with id {id_book} not found"), 404

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

#========================================================================================================

#CREATE A CATEGORY
@app.post('/category')
def create_category():
    data = request.get_json()
    category_name = data["category_name"]
    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.CREATE_CATEGORY_TABLE)
            cursor.execute(db.INSERT_INTO_CATEGORY, (category_name,))
        return "Category created successfully"
    

#SELECT ALL FROM CATEGORY
@app.get('/category')
def categories():
    all_categories = []
    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.SELECT_ALL_FROM_CATEGORY)
            result = cursor.fetchall()
            for category in result:
                all_categories.append({"category_id": category[0], "category_name":category[1]})
            return all_categories
            
#SELECT A CATEGORY BY ITS ID
@app.get('/category/<int:id_category>')
def get_category(id_category):
    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.SELECT_CATEGORY_BY_ID, (id_category,))
            
            if cursor.rowcount > 0:
                result_list = cursor.fetchone()
                result_json = {"category_id": result_list[0], "category_name": result_list[1]}
                return result_json, 200
            else:
                return(f"Category with id {id_category} does not exist"), 404
