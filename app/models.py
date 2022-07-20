from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow

ma = Marshmallow()
db = SQLAlchemy()


class Country(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<{self.name}>"


class City(db.Model):
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
    id = fields.Integer()
    date = fields.DateTime()
    temp_day = fields.String()
    temp_evening = fields.String()
    city_id = fields.Integer()
