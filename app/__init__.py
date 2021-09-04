from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.views import user_views
    user_views.init_app(app)

    return app
