# from flask import Flask
# from config import Config
# from flask_sqlalchemy import SQLAlchemy
#
#
#
# app = Flask(__name__)
# app.config.from_object(Config)
#
# db = SQLAlchemy()
# db.init_app(app)
#
#
# @app.before_first_request
# def create_table():
#     db.create_all()
#
#
# from app.weather.app import weather_bp
# app.register_blueprint(weather_bp, url_prefix='/weather')
from flask import Flask


def create_app(config_filename):
    app = Flask(__name__, static_folder="static")

    app.config.from_object(config_filename)

    from .models import db
    db.init_app(app)

    return app