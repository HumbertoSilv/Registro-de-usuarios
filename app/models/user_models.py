import os
import json
from dotenv import load_dotenv
from app.exc.exc import ExistingEmailError
load_dotenv()

DIRECTORY_DATABASE = os.getenv("DIRECTORY_DATABASE")


def create_db():
    if not os.path.isfile(DIRECTORY_DATABASE):
        os.makedirs("app/database/")
        with open(DIRECTORY_DATABASE, "x") as json_file:
            json.dump({"data": []}, json_file, indent=4)

    return True


create_db()

# if not os.path.isfile(DIRECTORY_DATABASE):
#     os.makedirs("app/database/")
#     with open(DIRECTORY_DATABASE, "x") as json_file:
#         json.dump({"data": []}, json_file, indent=4)


class User:
    def __init__(self, **kwargs) -> None:
        self.name: str = kwargs["nome"]
        self.email: str = kwargs["email"]

    @staticmethod
    def all_users():
        """Look for the .json file inside 'DIRECTORY_DATABASE' and display them."""
        create_db()

        with open(DIRECTORY_DATABASE, "r") as json_file:
            return json.load(json_file)

    def validate(**kwargs):
        create_db()
        email_type = type(kwargs["email"]) == str
        name_type = type(kwargs["nome"]) == str

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

        if not (name_type & email_type):
            result = []

            if not name_type:
                result.append({"name": types(kwargs["nome"])})

            if not email_type:
                result.append({"email": types(kwargs["email"])})

            return result

        with open("app/database/database.json", "r") as json_file:
            users_list = json.load(json_file)

        for email_list in users_list["data"]:
            if email_list["email"] == kwargs["email"].lower():
                raise ExistingEmailError

    def save(self):
        create_db()

        with open("app/database/database.json", "r") as json_file:
            users_list = json.load(json_file)

        users_list["data"].append({"nome": self.name.title(), "email": self.email.lower(), "id": len(users_list["data"])})

        with open("app/database/database.json", "w") as json_file:
            json.dump(users_list, json_file, indent=2)

        return {"data": users_list["data"][-1]}
