import datetime
from flask import Blueprint, render_template, request, flash
from app.models import City
from app.weather.utils import FutureTemperature, ArchiveTemperatureMonth
from app.weather.utils import CheckInputCity

weather_bp = Blueprint('weather', __name__)


@weather_bp.route("/")
def weather():
    """ Представления для главной страницы модуля """
    context = dict()
    context['title'] = 'Модуль "Погода"'
    return render_template("weather/weather.html", context=context)


@weather_bp.route("/future", methods=["POST", "GET"])
def future():
    """ Представления для прогноза погоды на две недели """
    context = dict()
    context['title'] = "Прогноз на 2 недели"

    if request.method == "POST":
        try:
            search_city = request.form.get('city')

            if search_city:
                cities = CheckInputCity().get_info_city(search_city)
                context['cities'] = cities

                if len(cities) == 1:
                    context['temps'] = FutureTemperature().get(cities[0].id)
                    context['title_city'] = cities[0].name

            case_city_id = request.form.get('radio')
            if case_city_id:
                context['temps'] = FutureTemperature().get(case_city_id)
                context['title_city'] = City.query.get(case_city_id).name

        except Exception as e:
            flash(f" {e} ")
    return render_template("weather/future.html", context=context)


@weather_bp.route("/archive", methods=["POST", "GET"])
def archive():
    """ Представления для архива погоды на месяц """
    context = dict()
    context['title'] = "Архив погоды на месяц"

    context['list_month'] = {"Выберите месяц": 0, "Январь": 1, "Февраль": 2,
                             "Март": 3, "Апрель": 4, "Май": 5, "Июнь": 6,
                             "Июль": 7, "Август": 8, "Сентябрь": 9,
                             "Октябрь": 10, "Ноябрь": 11, "Декабрь": 12}

    context['list_year'] = [year for year in range(2015, datetime.datetime.
                                                   today().year)]

    if request.method == "POST":
        try:
            archive_city = request.form.get('city')
            archive_year = request.form.get('list__year')
            archive_month = request.form.get('list__month')

            if archive_city:
                cities = CheckInputCity().get_info_city(archive_city)
                context['cities'] = cities
                if len(cities) == 1:
                    context['archive'] = ArchiveTemperatureMonth().\
                                        get_archive(city_id=cities[0].id,
                                                    year=int(archive_year),
                                                    month=int(archive_month))
                    context['title_city'] = cities[0].name

            case_city_id = request.form.get('radio')
            if case_city_id:
                context['archive'] = ArchiveTemperatureMonth().\
                                        get_archive(city_id=int(case_city_id),
                                                    year=int(archive_year),
                                                    month=int(archive_month))
                context['title_city'] = City.query.get(case_city_id).name

        except Exception as e:
            flash(f" {e} ")
    return render_template("weather/archive.html", context=context)
