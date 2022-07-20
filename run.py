from flask import render_template

from app import create_app
from config import Config

app = create_app(Config)

from app.models import db


@app.before_first_request
def create_table():
    db.create_all()
    # закомментировать после успешного первого старта программы
    # from app.load_start_data import save_data_in_db
    # save_data_in_db()


from app.weather.blueprint import weather_bp
from app.api.blueprint import api_bp

app.register_blueprint(weather_bp, url_prefix='/weather')
app.register_blueprint(api_bp, url_prefix='/api')


@app.route("/")
def index():
    """ Представление главной страницы """
    context = dict()
    context['title'] = "Home"
    return render_template("index.html", context=context)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
