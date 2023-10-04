from flask import Flask, request
app = Flask(__name__)
import uuid

books = [
    {
        "id": 1,
        "Title": "Title",
        "Authors": [
            {
                "id": "f5a7b2c3-8eab-4d9f-8f53-16f87f9a5d1a",
                "name": "name"
            },
            {
                "id": "9e1d65b7-3aef-4b16-a227-6c85d979e71f",
                "name": "name"
            }
        ],
        "Category": "Category",
        "Description": "Description",
        "ISBN": "ISBN",
        "Publishing-date": "Publishing-date",
        "Editorial": "Editorial"     
    }
]

#request book
@app.route("/books", methods = ["GET"])
def get_books():
    return books

#Create book
@app.route('/books', methods = ["POST"])
def create_book():
    data = request.get_json()
    new_book = {
    'id': len(books) + 1,
    'Title': data["Title"],
    'Authors': data["Authors"],
    'Category': data["Category"],
    'Description': data["Description"],
    'ISBN': data["ISBN"],
    'Publishing_date': data["Publishing-date"],
    'Editorial': data["Editorial"]
}

    for author in new_book["Authors"]:
        mi_uuid = uuid.uuid4()
        author['id'] = mi_uuid


    
    books.append(new_book)
    return books

#Update book
@app.route('/books/<int:id_book>',methods = ['PUT'])
def book_update(id_book):
    datos = request.get_json()
    for book in books:
        if book['id'] == id_book:
            book['Title'] = datos['Title']
            book['Authors'] = datos['Authors']
            book['Category'] = datos['Category']
            book['Description'] = datos['Description']
            book['ISBN'] = datos['ISBN']
            book['Publishing_date'] = datos['Publishing-date']
            book['Editorial'] = datos['Editorial']

            for author in book["Authors"]:
                mi_uuid = uuid.uuid4()
                author['id'] = mi_uuid

            return book
    return "Error:404 Book with that id not found"

#Delete book
@app.route('/books/<int:id_book>',methods = ['DELETE'])
def book_delete(id_book):
    for book in books:
        if book['id'] == id_book:
            books.remove(book)
            return f"Book with id {id_book} deleted successfully"
    return f"Error:404 Book with id {id_book} not found"


@app.route("/books/<string:category_chose>", methods =["GET"])

def request_category(category_chose):
    list_category = []
    for book_category in books:
        if book_category['Category'] == category_chose:
            list_category.append(book_category)
    if list_category:
        return list_category
        
    return f"Books of the category {category_chose} not found"


categories = [

    {
        "id": "1",
        "Category": "Fiction"
    },
    {
        "id": "2",
        "Category": "Non-Fiction"
    },
    {
        "id": "3",
        "Category": "Romance"
    },
    {
        "id": "4",
        "Category": "Science Fiction"
    },
    {
        "id": "5",
        "Category": "Mystery"
    },
    {
        "id": "6",
        "Category": "Fantasy"
    }
]





#¨Crud of category

@app.route("/categories", methods = ["GET"])
def request_categories():
    return categories

@app.route("/categories/create", methods = ["POST"])
def create_categories():
    data_categories = request.get_json()
    new_category = {
            "id": len(categories) + 1,
            "Category": data_categories["Category"]
            }

    categories.append(new_category)
    return new_category

@app.route("/categories/<int:id_update>", methods = ["PUT"])
def category_update(id_update):
    for item in categories:
        data_category = request.get_json()
        if item["id"] == id_update:
            item["Category"] = data_category["Category"]
            return f"Category with id {id_update} updated successfully"


    return f"Error:404 category with id {id_update} not found"
        

@app.route("/categories/delete/<int:num_delete>", methods = ["DELETE"])
def delete_category_item(num_delete):
    for item in categories:
        if item["id"] == num_delete:
            categories.remove(item)
            return f"Category with id {num_delete} deleted successfully"
    return f"Error:404 category with id {num_delete} not found"





