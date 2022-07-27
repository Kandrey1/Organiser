import datetime

from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow
from flask_login import UserMixin


ma = Marshmallow()
db = SQLAlchemy()


class Country(db.Model):
    """ Страны для модуля weather """
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<{self.name}>"


class City(db.Model):
    """ Города для модуля weather """
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    region = db.Column(db.String(200))
    name = db.Column(db.String(150))
    link = db.Column(db.String(250), unique=True)
    city_name = db.Column(db.String(150))
    city_num = db.Column(db.Integer)

    def __init__(self, country_id, region, name, link, city_name, city_num):
        self.country_id = country_id
        self.region = region
        self.name = name
        self.link = link
        self.city_name = city_name
        self.city_num = city_num

    def __repr__(self):
        return f"<{self.name} - {self.city_name} - {self.city_num}>"


class Temperature(db.Model):
    """ Температура в городе для модуля weather """
    __tablename__ = 'temperature'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    temp_day = db.Column(db.String(10))
    temp_evening = db.Column(db.String(10))

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))

    def __init__(self, date, city_id, temp_day, temp_evening):
        self.date = date
        self.city_id = city_id
        self.temp_day = temp_day
        self.temp_evening = temp_evening

    def __repr__(self):
        return f"<{self.date} - {self.city_id} - {self.temp_day} -" \
               f" {self.temp_evening}>"


class TemperatureSchema(ma.Schema):
    """ Shema для модуля Temperature """
    id = fields.Integer()
    date = fields.DateTime()
    temp_day = fields.String()
    temp_evening = fields.String()
    city_id = fields.Integer()


class User(UserMixin, db.Model):
    """ Пользователи приложения """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    todo = db.relationship('TodoList', backref='User', uselist=True,
                           lazy=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<{self.name} - {self.email}>"


class TodoList(db.Model):
    """ Список дел """
    __tablename__ = 'todo_list'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    create = db.Column(db.DateTime, default=datetime.datetime.today())

    boss_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status_boss = db.Column(db.Boolean, default=False)
    worker_id = db.Column(db.Integer)
    status_worker = db.Column(db.Boolean, default=False)

    def __init__(self, name, boss_id, status_boss, worker_id, status_worker):
        self.name = name
        self.boss_id = boss_id
        self.status_boss = status_boss
        self.worker_id = worker_id
        self.status_worker = status_worker

    def __str__(self):
        return f"<{self.name}>"


class UserFriend(db.Model):
    """ Друзья пользователя """
    __tablename__ = 'user_friend'

    id = db.Column(db.Integer, primary_key=True)
    friend_one = db.Column(db.Integer)
    friend_two = db.Column(db.Integer)

    def __init__(self, friend_one, friend_two):
        self.friend_one = friend_one
        self.friend_two = friend_two

    def __str__(self):
        return f"<{self.friend_one} - {self.friend_two}>"


class ShopList(db.Model):
    """ Список покупок """
    __tablename__ = 'shop_list'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    create = db.Column(db.DateTime, default=datetime.datetime.today())
    check = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, check, user_id):
        self.name = name
        self.check = check
        self.user_id = user_id

    def __str__(self):
        return f"<{self.name}>"
