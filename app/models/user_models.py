import os
import json
from dotenv import load_dotenv
from app.exc.exc import ExistingEmailError, TypeConflictError, EmailError, NameError
load_dotenv()

DIRECTORY_DATABASE = os.getenv("DIRECTORY_DATABASE")


if not os.path.isfile(DIRECTORY_DATABASE):
    os.makedirs("app/database/")
    with open(DIRECTORY_DATABASE, "x") as json_file:
        json.dump({"data": []}, json_file, indent=4)


class User:
    def __init__(self, **kwargs) -> None:
        self.name: str = kwargs["nome"]
        self.email: str = kwargs["email"]

    @staticmethod
    def all_users():
        """Look for the .json file inside 'DIRECTORY_DATABASE' and display them."""
        if not os.path.isfile(DIRECTORY_DATABASE):
            os.makedirs("app/database/")
            with open(DIRECTORY_DATABASE, "x") as json_file:
                json.dump({"data": []}, json_file, indent=4)

        with open(DIRECTORY_DATABASE, "r") as json_file:
            return json.load(json_file)

    def validate(**kwargs):
        email_type = type(kwargs["email"]) == str
        name_type = type(kwargs["nome"]) == str

        if not name_type:
            raise NameError

        if not email_type:
            raise EmailError

        with open("app/database/database.json", "r") as json_file:
            users_list = json.load(json_file)

        for email_list in users_list["data"]:
            if email_list["email"] == kwargs["email"].lower():
                raise ExistingEmailError

    def save(self):
        if not os.path.isfile(DIRECTORY_DATABASE):
            os.makedirs("app/database/")
            with open(DIRECTORY_DATABASE, "x") as json_file:
                json.dump({"data": []}, json_file, indent=4)

        with open("app/database/database.json", "r") as json_file:
            users_list = json.load(json_file)

        users_list["data"].append({"nome": self.name.title(), "email": self.email.lower(), "id": len(users_list["data"])})

        with open("app/database/database.json", "w") as json_file:
            json.dump(users_list, json_file, indent=2)

        return {"data": users_list["data"][-1]}
