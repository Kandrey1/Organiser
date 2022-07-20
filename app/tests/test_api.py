import requests


def test_api_future():
    city = 'москва'
    get = requests.get(
        f'http://127.0.0.1:5000/api/weather/future/{city}')

    assert get


def test_api_archive():

    data = {"city": "смоленск", "year": 2019, "month": 4}
    get = requests.get(
        f'http://127.0.0.1:5000/api/weather/archive', json=data)

    assert get
