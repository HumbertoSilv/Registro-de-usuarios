from flask import Flask, request
from app.models.user_models import User
from app.exc.exc import ExistingEmailError, NameError, EmailError


def init_app(app: Flask):
    @app.get("/user")
    def get_user():
        users = User.all_users()

        return users

    @app.post("/user")
    def create_user():
        data = request.json

        try:
            User.validate(**data)
            user = User(**data)
            saved = user.save()

        except ExistingEmailError as msg:
            return str(msg), 409

        except NameError:

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

            return {"wrong fields": [{"nome": types(data["nome"])}]}, 400

        except EmailError:

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

            return {"wrong fields": [{"email": types(data["email"])}]}, 400

        return saved, 201
