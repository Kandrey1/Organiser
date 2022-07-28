# Organiser
Web приложение "Органайзер", на данный момент включает в себя полезные функции: погода, список дел(с возможностью делегации), список покупок.

В основе -  ЯП: Python, фреймворк: Flask, SQL : SQLAlchemy (sqlite3).

## Технологий
- Python 3.7.5
- Flask 2.1.3
- Flask-RESTful 0.3.9
- Flask-SQLAlchemy 2.5.1
- SQLAlchemy 1.4.39
- beautifulsoup4 4.11.1
- pandas 1.3.5
- pytest 7.1.2

## Реализовано
- ### Модуль weather
    - Показывает прогноз погоды на две недели
    - Показывает архив погоды за месяц

  
  Принцип: При первой загрузке приложения создается БД со списком городов. Прогноз на 2 недели парсится с сайта. 
  Архив на месяц берется из БД, если в ней нет нужного архива, то архив парсится и сохраняется в БД. 
  
 Данный модуль работает без авторизации в приложении.   
 
- ### Модуль User
    Позволяет авторизоваться на сайте. Остальные модули отображаются только после авторизации. Обеспечивает изоляцию данных от других пользователей.

    
- ### REST API Flask
  Get запрос через url. Получить прогноз погоды на две недели по названию города

  `127.0.0.1/api/weather/future/"название города"`

    Get запрос с помощью json формата {"city":"","year":"","month":""}. Получить архив погоды за месяц
    
  `127.0.0.1/api/weather/archive`
    
    Если городов с названием больше одного, возвращает данные на каждый город.
 
- ### Модуль Todo
    - Создает список дел(задач). Реализована возможность поручать задачи другим пользователям(друзьям)
    - Создает список покупок
  
  Принцип: При первой загрузке приложения создается БД со списком городов. Прогноз на 2 недели парсится с сайта. 
  Архив на месяц берется из БД, если в ней нет нужного архива, то архив парсится и сохраняется в БД. 

## Установка

Перейти в корень collections_flask и выполнить следующий команды:

Для установки необходимых модулей

`pip install -r requirements.txt`

Для запуска в командной строке, находясь в корне выполнить:

`python run.py`

В браузере перейти и дождаться загрузки (Создается БД и в нее сохраняется список городов)

`http://127.0.0.1:5000/`

После успешной загрузки страницы в браузере установить в БД начальные данные (список городов и стран) командой:

 `python set_start_data.py`
 
