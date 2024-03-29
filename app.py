from flask import Flask, request, jsonify
import data.db as db
import jwt
from datetime import datetime, timedelta
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
            books_dict.append({"id": row[0], "title": row[1], "category": row[2]})
        return json.dumps(books_dict)


# GET A BOOK BY ITS ID
@app.get("/books/<int:id_row>")
def get_book(id_row):
    with db.connection_pool.connect() as db_conn:
        result_row = db_conn.execute(db.GET_A_BOOK, parameters={"book_id": id_row}).fetchone()
        if result_row is not None:
            result_json = {"id": result_row[0], "title": result_row[1], "category": result_row[2]}
            return json.dumps(result_json), 200
        else:
            return f"Error: Book with id {id_row} not found", 404


# UPDATE A BOOK
@app.put("/books/<int:id_book>")
def book_update(id_book):
    data = request.get_json()
    title = data["title"]
    category = data["category"]

    with db.connection_pool.connect() as db_conn:
        result = db_conn.execute(db.UPDATE_BOOK, parameters={"title": title, "category": category, "book_id": id_book})
        db_conn.commit()
        if result.rowcount > 0:
            return f"Book with id {id_book} updated successfully", 200
        else:
            return f"Error 404: Book with id {id_book} not found", 404


# Delete book
@app.delete('/books/<int:id_book>')
def book_delete(id_book):
    with db.connection_pool.connect() as db_conn:
        result = db_conn.execute(db.DELETE_BOOK, parameters={"id_book": id_book})
        db_conn.commit()
        if result.rowcount > 0:
            return "book deleted successfully", 200
        else:
            return f"Book with id {id_book} not found", 404


# ========================================================================================================

# CREATE A CATEGORY
@app.post('/category')
def create_category():
    data = request.get_json()
    category_name = data["category_name"]
    with db.connection_pool.connect() as db_conn:
        db_conn.execute(db.CREATE_CATEGORY_TABLE)
        db_conn.execute(db.INSERT_INTO_CATEGORY, parameters= {"category_name": category_name})
        db_conn.commit()
    return "Category created successfully", 200


# SELECT ALL FROM CATEGORY
@app.get('/category')
def categories():
    all_categories = []
    with db.connection_pool.connect() as db_conn:
        result = db_conn.execute(db.SELECT_ALL_FROM_CATEGORY).fetchall()
        for category in result:
            all_categories.append({"category_id": category[0], "category_name": category[1]})
        return json.dumps(all_categories)

# SELECT A CATEGORY BY ITS ID
@app.get('/category/<int:id_category>')
def get_category(id_category):
    with db.connection_pool.connect() as db_conn:
        result = db_conn.execute(db.SELECT_CATEGORY_BY_ID, parameters= {"id": id_category}).fetchone()
        db_conn.commit()

        if result is not None:
            result_json = {"category_id": result[0], "category_name": result[1]}
            return json.dumps(result_json), 200
        else:
            return f"Category with id {id_category} does not exist", 404

# UPDATE A CATEGORY
@app.put('/category/<int:id_category>')
def update_category(id_category):
    data = request.get_json()
    category_name = data["category_name"]
    with db.connection_pool.connect() as db_conn:
        result = db_conn.execute(db.UPDATE_CATEGORY, parameters= {"name": category_name , "id": id_category})
        db_conn.commit()
        if result.rowcount > 0:
            return f"Category with id {id_category} was updated successfully", 200
        else:
            return f"Category with id {id_category} does not exist", 404

# DELETE A CATEGORY
@app.delete('/category/<int:id_category>')
def remove_category(id_category):
    with db.connection_pool.connect() as db_conn:
        result = db_conn.execute(db.DELETE_CATEGORY, parameters = {"id": id_category})
        db_conn.commit()
        if result.rowcount > 0:
            return f"Category with id {id_category} deleted", 200
        else:
            return f"Category with id {id_category} does not exist", 404

# ========================================================================================================
# TOKEN GENERATOR
def jwt_converter(data):
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload_data = data
    secret_key = "ThisIsTheSecretKey"

    token = jwt.encode(payload_data, secret_key, algorithm='HS256', headers=header)
    return token

# CREATE_USER
@app.post("/user")
def create_user():
    data = request.get_json()
    data_for_token = {"name": data["name"], "lastname": data["lastname"], "username": data["username"]}

    token = jwt_converter(data_for_token)

    with db.connection_pool.connect() as db_conn:
        db_conn.execute(db.CREATE_USER)

        result = db_conn.execute(db.INSERT_INTO_USER, parameters = {
            "name": data["name"], "lastname": data["lastname"], "username": data["username"], "email": data["email"], "password": data["password"], "created_at": data["created_at"],
            "token": token})
        db_conn.commit()

        if result.rowcount > 0:
            return f"Account created Successfully, Your authentication token is \n{token}\n", 200
        else:
            return f"Something went bad, check your credentials and try again"

# GET ALL THE USERS
@app.get("/accounts")
def request_users():
    with db.connection_pool.connect() as db_conn:
        accounts = db_conn.execute(db.GET_ALL_USER).fetchall()
        accounts_list = []

        for user in accounts:
            accounts_list.append(
                {"name": user[0], "lastname": user[1], "username": user[2], "email": user[3], "password": user[4],
                 "created_at": user[5]})
        return accounts_list, 200


# GET A USER
@app.get("/user")
def request_a_user():
    data = request.headers.get('Authorization')
    token = data.split(' ')[1]
    with db.connection_pool.connect() as db_conn:
        data_result = db_conn.execute(db.GET_A_USER, parameters = {"Token": token}).fetchone()
        db_conn.commit()

        if data_result is not None:
            data_json = {"name": data_result[0], "lastname": data_result[1], "username": data_result[2], "email": data_result[3],
                         "password": data_result[4], "created_at": data_result[5], "update_at": data_result[6]}

            return data_json, 200
        else:
            return "Unauthorized access", 401


# UPDATE A USER
@app.put("/user")
def update_password():
    data = request.get_json()
    current_password = data["current_password"]
    new_password = data["new_password"]
    username = data["username"]
    update_at = data["update_at"]
    data_token = request.headers.get('Authorization')
    token = data_token.split(' ')[1]

    with db.connection_pool.connect() as db_conn:
        result = db_conn.execute(db.UPDATE_USER, parameters= {"password": new_password, "update_at": update_at, "token":token, "current_password": current_password, "username": username})
        db_conn.commit()
        if result.rowcount > 0:
            return "User updated successfully", 200
        else:
            return "Unauthorized access", 401


# DELETE A USER
@app.delete("/user")
def delete_user():
    data = request.headers.get('Authorization')
    token = data.split(' ')[1]
    print(token)
    with db.connection_pool.connect() as db_conn:
        result = db_conn.execute(db.DELETE_USER, parameters= {"token":token})
        db_conn.commit()
        if result.rowcount > 0:
            return "User account delete successfully", 200
        else:
            return "Unauthorized access", 401

#User_Login
@app.post('/login')
def user_login():
    def token_creator(user, passw):
        header = {
            "alg": "HS256",
            "typ": "JWT",
            "exp": (datetime.utcnow() + timedelta(days=1)).isoformat()
        }

        payload = {"username": user, "password": passw}
        secret_key = "ThisIsTheSecretKey"

        token = jwt.encode(payload, secret_key, algorithm='HS256', headers=header)
        return token

    data = request.get_json()
    username =  data['username']
    password = data['password']
    with db.connection_pool.connect() as db_conn:
        result = db_conn.execute(db.USER_LOGIN, parameters = {"pass": password, "user": username})
        db_conn.commit()
        if result.rowcount > 0:
            #Make and change the JWT
            token_created = token_creator(user=username, passw=password)
            with db.connection_pool.connect() as db_connection:
                db_connection.execute(db.ADD_TOKEN, parameters= {"token": token_created, "user": username, "pass": password})
                db_connection.commit()
                return f"Successful login. Your authentication token is\n\n\t{token_created}", 200
        else:
            return "Unauthorized: Invalid username or password.", 401