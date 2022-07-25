from flask import Flask
from flask_login import LoginManager


def create_app(config_filename):
    app = Flask(__name__, static_folder="static")

    app.config.from_object(config_filename)

    from .models import db
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app