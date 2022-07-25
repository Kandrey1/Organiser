from ..weather.utils import FutureTemperature, ArchiveTemperatureMonth
from ..weather.parser_weather import ConnectSite, ParserWeather
from run import client

# ---------------------------- Parser_weather ----------------------------------
def test_parser_connect():
    url = "https://www.gismeteo.ru/weather-moscow-4368/"
    data = ConnectSite().get_soup_page(url)

    assert data


def test_parser_future_1():
    url = "https://www.gismeteo.ru/weather-moscow-4368/2-weeks/"
    data = ParserWeather().future_temperature(url)

    assert len(data) == 14
    assert data[12]['date']


def test_parser_future_2():
    url = "https://www.gismeteo.ru/weather-saransk-4401/2-weeks/"
    data = ParserWeather().future_temperature(url)

    assert len(data) == 14
    assert data[12]['date']


def test_parser_archive_1():
    url = "https://www.gismeteo.ru/diary/11447/2020/2/"
    data = ParserWeather().archive_temperature(url)

    assert data[10]['date'].day == 11
    assert data[9]['temperature_daytime'] == '+3'
    assert len(data) == 29
    assert data[25]['temperature_evening'] == '+2'


def test_parser_archive_2():
    url = "https://www.gismeteo.ru/diary/5032/2016/5/"
    data = ParserWeather().archive_temperature(url)

    assert data[3]['date'].day == 4
    assert data[6]['temperature_daytime'] == '+22'
    assert len(data) == 31
    assert data[24]['temperature_evening'] == '+21'
# ---------------------------- Parser_weather ----------------------------------
# ---------------------------- Utils -------------------------------------------

def test_utils_cls_future_create_url():
    url = FutureTemperature()
    url.city_name = 'kursk'
    url.city_num = 5010
    url._create_url()

    assert url._url == "https://www.gismeteo.ru/weather-kursk-5010/2-weeks/"

    # ------------------------------------
    url = FutureTemperature()
    url.city_name = 'kazan'
    url.city_num = 4364
    url._create_url()

    assert url._url == "https://www.gismeteo.ru/weather-kazan-4364/2-weeks/"


# def test_utils_cls_future_get():
#     pass


def test_utils_cls_archive_create_url():
    url = ArchiveTemperatureMonth()
    url.city_num = 4787
    url.year = 2014
    url.month = 10
    url._create_url()

    assert url._url == "https://www.gismeteo.ru/diary/4787/2014/10/"


# def test_utils_cls_archive_get_archive():
#     pass


# def test_utils_cls_archive_save_month():
#     pass

# ---------------------------- Utils -------------------------------------------

def test_rout_weather():
    res = client.get('/weather/')

    assert res.status_code == 200


def test_rout_future():
    res = client.get('/weather/future')

    assert res.status_code == 200


def test_rout_archive():
    res = client.get('/weather/archive')

    assert res.status_code == 200

