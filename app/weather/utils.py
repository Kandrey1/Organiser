import datetime
import re
from ..models import City, Temperature
from .parser_weather import ParserWeather


class CustomErrorNotDb(Exception):
    pass


class FutureTemperature:
    """ Прогноз погоды на две недели.
        get: получает id города и возвращает словарь с погодой на 2 недели
            city_id: id города, для прогноза погоды.
    """
    def __init__(self):
        self._host = 'https://www.gismeteo.ru'
        self.city_name = ''
        self.city_num = ''
        self.city_id = ''
        self._future_temp = list()

    def _create_url(self):
        """ Создает конечный url страницы с прогнозом погоды"""
        self._url = f"{self._host}/" \
                    f"weather-{self.city_name}-{self.city_num}/2-weeks/"

    def get(self, city_id: int) -> list:
        """ Возвращает словарь с прогнозом погоды.
            city_id: int - id города для прогноза.
        """
        try:
            self.city_id = city_id
            city = City.query.get(self.city_id)
            self.city_name = city.city_name
            self.city_num = city.city_num
            self._create_url()
            self._future_temp = ParserWeather().future_temperature(self._url)
        except Exception as e:
            print("Ошибка в классе FutureTemperature", f"<{e}>")
        return self._future_temp


class ArchiveTemperatureMonth:
    """ Архив температуры за месяц.
        _create_url: создает url на страницу архива.
        request_archive: Возвращает архива по запросу аргументов.
            city: город равный city_num из БД.
            year: год который нужно найти.
            month: месяц который нужно найти.
        save_archive_month: сохраняет спарсеный архив в БД.
        get_archive: возвращает архив в словаре(возвращает пустой словарь
            если не было правильного request_archive.
    """
    def __init__(self):
        self._host = 'https://www.gismeteo.ru/diary'
        self._archive = dict()
        self.archive_db = dict()
        self.city_id = int()
        self.city_num = int()
        self.year = int()
        self.month = int()
        self.archive_db = dict()

    def _create_url(self):
        """ Создает url на страницу архива"""
        self._url = f"{self._host}/{self.city_num}/{self.year}/{self.month}/"

    def _parsing_archive(self):
        """ Парсит архив с сайта. И возвращает его в словаре. """
        self._create_url()
        self._archive = ParserWeather().archive_temperature(self._url)
        self._save_archive_month()

    def _save_archive_month(self):
        """ Сохраняет спарсеный архив в БД """
        try:
            from run import app
            from app.models import db, Temperature
            # не уверен, что правильный вариант
            db.session.close()
            with app.app_context():
                for row in self._archive:
                    temperature = Temperature(
                        date=row['date'],
                        temp_day=row['temperature_daytime'],
                        temp_evening=row['temperature_evening'],
                        city_id=self.city_id)
                    db.session.add(temperature)
                db.session.commit()
        except Exception as e:
            print("Ошибка сохранения в БД", f"<{e}>")

    def _check_temperarure_db(self):
        """ Проверяет есть в БД записи о температуре за искомый период """
        date_1 = datetime.datetime(self.year, self.month, 5)
        check_date = Temperature.query.filter(
                                        Temperature.city_id == self.city_id,
                                        Temperature.date == date_1).all()
        return True if check_date else False

    def get_archive(self, city_id: int, year: int, month: int) -> list:
        """ Возвращает архив(словарь) с погодой на месяц.
            city_id: int - id города
            year: int - год архива
            month: int - месяц архива
        """
        try:
            self.city_id = city_id
            self.city_num = City.query.get(self.city_id).city_num
            self.year = year
            self.month = month

            if not self._check_temperarure_db():
                self._parsing_archive()

            date_start = datetime.date(self.year, self.month, 1)
            date_end = datetime.date(self.year, self.month + 1, 1)
            self.archive_db = Temperature.query.filter(
                           Temperature.city_id == self.city_id,
                           Temperature.date.between(date_start, date_end)).all()
        except Exception as e:
            print("Ошибка в классе ArchiveTemperatureMonth", f"<{e}>")
        return self.archive_db


class CheckInputCity:
    """ Проверяет строку введенного значения города. Если строка существует
        и она корректная, то она форматируется и ищется совпадение в БД.
    """
    def _check_str(self):
        """ Проверяет корректность введенного названия города"""
        if self.str_input:
            pattern = r'[а-яА-Я-]+'
            if not re.fullmatch(pattern, self.str_input):
                raise ValueError('Введенные данные некорректны')
        else:
            raise ValueError('Вы ничего не ввели')
        return True

    def _format_city(self):
        """ Форматирует название города.(Переводит первый символ строки
            в верхний регистр).
        """
        # TODO переработать форматирование
        # если город состоит из двух частей вторую часть надо capitalaze
        # как вариант разбить по дефису, capitalase и соединить
        # пока форматирование только для города из одного слова
        self.str_input = self.str_input.capitalize()

    def get_info_city(self, str_input):
        """ Возвращает объект cities из таблицы в БД. Если строка пустая или
            некорректная, то возвращает ошибку.
        """
        self.str_input = str_input.strip()
        if self._check_str():
            self._format_city()
            cities = City.query.filter(City.name == self.str_input).all()
            if not cities:
                raise CustomErrorNotDb('В база нет такого города')
            return cities
