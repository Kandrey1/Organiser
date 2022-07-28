from flask import render_template

from app import create_app
from config import Config

app = create_app(Config)

client = app.test_client()

from app.models import db


@app.before_first_request
def create_table():
    db.create_all()


from app.weather.blueprint import weather_bp
from app.api.blueprint import api_bp
from app.user.blueprint import user_bp
from app.todo.blueprint import todo_bp

app.register_blueprint(weather_bp, url_prefix='/weather')
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(todo_bp, url_prefix='/todo')


@app.route("/")
def index():
    """ Представление главной страницы """
    context = dict()
    context['title'] = "Home"
    return render_template("index.html", context=context)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
