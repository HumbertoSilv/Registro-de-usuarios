from flask import Flask, request, jsonify
import os
import json


if not os.path.isfile("app/database/database.json"):
    os.makedirs("app/database/")
    with open("app/database/database.json", "x") as json_file:
        json.dump({"data": []}, json_file, indent=4)

app = Flask(__name__)


@app.get("/user")
def get_user():
    if os.path.isfile("app/database/database.json"):
        with open("app/database/database.json", "r") as json_file:
            return json.load(json_file)


@app.post("/user")
def create_user():
    name: str = request.json["name"]
    email: str = request.json["email"]
    email_type = type(email) == str
    name_type = type(name) == str

    def types(value):
        if type(value) == str:
            return "string"
        if type(value) == dict:
            return "dictionary"
        if type(value) == int:
            return "integer"
        if type(value) == list:
            return "list"
        if type(value) == float:
            return "float"

    if not (email_type & name_type):
        return {"wrong fields": [{"name": types(name)}, {"email": types(email)}]}, 400

    with open("app/database/database.json", "r") as json_file:
        users_list = json.load(json_file)

    for email_list in users_list["data"]:
        if email_list["email"] == email.lower():
            return {"error": "User already exists."}, 409

    users_list["data"].append({"name": name.title(), "email": email.lower(), "id": len(users_list["data"])})

    with open("app/database/database.json", "w") as json_file:
        json.dump(users_list, json_file, indent=2)

    return jsonify({"data": users_list["data"][-1]}), 201
