from flask import Flask, request, jsonify
import jwt
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

information = [{
    "id": "id",
    "name": "name",
    "lastname": "lastname",
    "username": "username",
    "token": "",
    "Password": "password"
}]


#Function token converter
def token_converter(information):
    payload_data = information

    token = jwt.encode(
        payload=payload_data,
        key="my_super_secret",
        algorithm='HS256'

    )

    information["token"] = token

#Request account
@app.route('/account', methods=['GET'])
def request_account():
    return information

#Create account
@app.route('/account', methods=['POST'])
def create_account():
    dato = request.get_json()
    new_account = {
        "id": len(information) + 1,
        "name": dato["name"],
        "lastname": dato["lastname"],
        "username": dato["username"],
        "token": "",
        "password": dato["password"]
    }
    information.append(new_account)
    token_converter(new_account)
    return jsonify(new_account)

#Update account
@app.route('/account/<int:id_user>', methods=['PUT'])
def update_account(id_user):
    data_updated = request.get_json()
    for account_update in information:
        if account_update['id'] == id_user:
            account_update['name'] = data_updated["name"]
            account_update['lastname'] = data_updated["lastname"]
            account_update['username'] = data_updated["username"]
            account_update['token'] = data_updated["token"]
            account_update['password'] = data_updated["password"]
            token_converter(account_update)
            return jsonify(account_update)
    return f"Account with id {id_user} not found"

#Delete account
@app.route('/account/<int:id_delete>', methods=['DELETE'])
def delete_account(id_delete):
    for account in information:
        if account['id'] == id_delete:
            information.remove(account)
            return "Account deleted successfully"

    return f"Account with id {id_delete} not found"

