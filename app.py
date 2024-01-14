from flask import Flask, request, jsonify
import data.db as db
import jwt
import json
import sqlalchemy
from cryptography.hazmat.primitives import serialization

db.init_database()
app = Flask(__name__)


# CREATE BOOK
@app.post('/books')
def create_book():
    data = request.get_json()
    title = data["title"]
    category = data["category"]

    with db.connection_pool.connect() as db_conn:
        db_conn.execute(db.CREATE_BOOK_TABLE)
        db_conn.execute(db.INSERT_INTO_BOOK_TABLE, parameters={"title": title, "category": category})
        db_conn.commit()
    return "book created successfully", 200


# GET ALL THE BOOKS CONTENT
@app.get("/books")
def get_books():
    with db.connection_pool.connect() as db_conn:
        result = db_conn.execute(db.GET_ALL_THE_BOOKS).fetchall()
        books_dict = []
        for row in result:
            books_dict.append({"id":row[0], "title": row[1], "category":row[2]})
        return json.dumps(books_dict)



# GET A BOOK BY ITS ID
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


# UPDATE A BOOK
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


# Delete book
@app.delete('/books/<int:id_book>')
def book_delete(id_book):
    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.DELETE_BOOK, (id_book,))

            if cursor.rowcount > 0:
                return "book deleted successfully"
            else:
                return (f"Book with id {id_book} not found"), 404


# ========================================================================================================

# CREATE A CATEGORY
@app.post('/category')
def create_category():
    data = request.get_json()
    category_name = data["category_name"]
    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.CREATE_CATEGORY_TABLE)
            cursor.execute(db.INSERT_INTO_CATEGORY, (category_name,))
        return "Category created successfully"


# SELECT ALL FROM CATEGORY
@app.get('/category')
def categories():
    all_categories = []
    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.SELECT_ALL_FROM_CATEGORY)
            result = cursor.fetchall()
            for category in result:
                all_categories.append({"category_id": category[0], "category_name": category[1]})
            return all_categories


# SELECT A CATEGORY BY ITS ID
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
                return (f"Category with id {id_category} does not exist"), 404


# UPDATE A CATEGORY
@app.put('/category/<int:id_category>')
def update_category(id_category):
    data = request.get_json()
    category_name = data["category_name"]
    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.UPDATE_CATEGORY, (category_name, id_category))
            if cursor.rowcount > 0:
                return f"Category with id {id_category} was updated successfully", 200
            else:
                return f"Category with id {id_category} does not exist", 404


# DELETE A CATEGORY
@app.delete('/category/<int:id_category>')
def remove_category(id_category):
    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.DELETE_CATEGORY, (id_category,))
            if cursor.rowcount > 0:
                return f"Category with id {id_category} deleted", 200

            else:
                return f"Category with id {id_category} does not exist", 404


# ========================================================================================================
# TOKEN GENERATOR
def jwt_converter(datos):
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload_data = datos
    secret_key = "ThisIsthesecretkey"

    token = jwt.encode(payload_data, secret_key, algorithm='HS256', headers=header)
    return token


# CREATE_USER
@app.post("/user")
def create_user():
    data = request.get_json()
    data_for_token = {"name": data["name"], "lastname": data["lastname"], "username": data["username"]}

    token = jwt_converter(data_for_token)

    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.CREATE_USER)
            cursor.execute(db.INSER_INTO_USER, (
            data["name"], data["lastname"], data["username"], data["email"], data["password"], data["created_at"],
            token))

            if cursor.rowcount > 0:
                return f"Account created Successfully And the jwt is \n{token}\n", 200
            else:
                return f"something went wrong"


# GET ALL THE USERS
@app.get("/user")
def request_users():
    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.GET_ALL_USER)
            accounts = cursor.fetchall()
            users = []

            for user in accounts:
                users.append(
                    {"name": user[0], "lastname": user[1], "username": user[2], "email": user[3], "password": user[4],
                     "created_at": user[5]})
            return users


# GET A USER
@app.get("/user/<string:token>")
def request_a_user(token):
    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.GET_A_USER, (token,))
            if cursor.rowcount > 0:
                data = cursor.fetchone()
                data_json = {"name": data[0], "lastname": data[1], "username": data[2], "email": data[3],
                             "password": data[4], "created_at": data[5], "update_at": data[6]}

                return data_json, 200
            else:
                return "Unauthorized access", 401


# UPDATE A USER
@app.put("/user/<string:token>")
def update_password(token):
    data = request.get_json()
    current_password = data["current_password"]
    new_password = data["new_password"]
    username = data["username"]
    update_at = data["update_at"]

    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.UPDATE_USER, (new_password, update_at, token, current_password, username,))
            if cursor.rowcount > 0:
                return "User updated successfully", 200
            else:
                return "Unauthorized access", 401


# DELETE A USER
@app.delete("/user/<string:token>")
def delete_user(token):
    with db.connection:
        with db.connection.cursor() as cursor:
            cursor.execute(db.DELETE_USER, (token,))
            if cursor.rowcount > 0:
                return "User account delete successfully", 200
            else:
                return "Unauthorized access", 401
