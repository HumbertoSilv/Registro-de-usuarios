from flask import Flask, request
from app.models.user_models import User
from app.exc.exc import ExistingEmailError, NameError, EmailError, TypeConflictError


def init_app(app: Flask):
    @app.get("/user")
    def get_user():
        users = User.all_users()

        return users

    @app.post("/user")
    def create_user():
        data = request.json

        try:
            validate = User.validate(**data)
            if validate:
                return {"wrong fields": validate}, 400

            user = User(**data)
            saved = user.save()

        except ExistingEmailError as msg:
            return str(msg), 409

        return saved, 201
