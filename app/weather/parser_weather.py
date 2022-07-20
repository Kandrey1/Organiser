import datetime
import requests
from bs4 import BeautifulSoup


class ConnectSite:
    """ Подключение к сайту и получение страницы в формате BeautifulSoup """
    def get_soup_page(self, url_page: str):
        """ Возвращает страницу.
            url_page: url адрес страницы
        """
        headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/39.0.2171.95 Safari/537.36'}

        page = requests.get(url_page, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup


class ParserWeather:
    """ Парсер страниц.
        archive_temperature: парсит архив погоды за указанный месяц
        future_temperature: парсит погоду на две недели вперед
    """
    def archive_temperature(self, url_page: str) -> list:
        """ Возвращает архив погоды на месяц
            url_page: url страницы с архивом.
        """
        archive = []

        try:
            url_split = url_page.split('/')

            soup = ConnectSite().get_soup_page(url_page)

            rows_archive = soup.findAll('tr', {'align': 'center'})

            for row in rows_archive:
                # date
                date_day = row.find('td', {'class': 'first'})
                date_f = datetime.date(int(url_split[-3]),
                                       int(url_split[-2]),
                                       int(date_day.text))

                # temperature_daytime and temperature_evening
                temperature_day = row.findAll('td', {'class': 'first_in_group'})

                row_archive = {'date': date_f,
                               'temperature_daytime': temperature_day[0].text,
                               'temperature_evening': temperature_day[1].text
                               }
                archive.append(row_archive)

        except Exception as e:
            print("Не удалось получить страницу архива", f"<{e}>")

        return archive

    def future_temperature(self, url_page: str) -> list:
        """ Возвращает температуру на 14 дней вперед
            url_page: url страницы с прогнозом погоды.
        """
        future = dict()
        future_format = list()
        days = 14
        try:
            future['date'] = []
            future['temperature_daytime'] = []
            future['temperature_evening'] = []
            future['rain'] = []

            soup = ConnectSite().get_soup_page(url_page)

            temperature_blog = soup.find('div', {'class': 'widget-items'})
            # date
            dates = temperature_blog.findAll('div', {'class': 'date'})[:days]
            for date in dates:
                future['date'].append(date.text)
            # temperature_daytime
            daytimes = temperature_blog.findAll('div', {'class': 'maxt'})[:days]
            for daytime in daytimes:
                future['temperature_daytime'].append(daytime.contents[0].text)
            # temperature_evening
            evenings = temperature_blog.findAll('div', {'class': 'mint'})[:days]
            for evening in evenings:
                future['temperature_evening'].append(evening.contents[0].text)
            # rain
            rains = temperature_blog.findAll('div',
                                     {'class': 'weather-icon tooltip'})[:days]
            for rain in rains:
                future['rain'].append(rain.attrs['data-text'])

            future_format = self._format_data_future(future)

        except Exception as e:
            print("Не удалось получить прогноз на 2 недели", f"<{e}>")
        return future_format

    def _format_data_future(self, data_dict: dict) -> list:
        """ Форматирует входящий словарь с прогноза погоды на 2 недели в
            формат [{}, {}, ...], где словарь это данные по одному дню.
        """
        data_format = []
        for i in range(len(data_dict['date'])):
            item = {'date': data_dict['date'][i],
                    't_day': data_dict['temperature_daytime'][i],
                    't_evening': data_dict['temperature_evening'][i],
                    'rain': data_dict['rain'][i]
                    }
            data_format.append(item)
        return data_format
