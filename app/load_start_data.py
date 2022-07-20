"""
Сохраняет в БД данные из файлов cities.csv и country.csv.
"""
import pandas as pd
# from models import db, Country, City


path_start_file = 'app/data/'


def save_countries_db():
    """ Сохраняет данные из файла country.csv в таблицу в БД """
    from run import app
    from app.models import db, Country
    db.session.close()
    try:
        df_country = pd.read_csv(f'{path_start_file}country.csv')
        countries = df_country.country.to_list()
        with app.app_context():
            for country in countries:
                count = Country(name=country)
                db.session.add(count)
            db.session.commit()
        print("Таблица country успешно сохранена в БД")
    except Exception as e:
        db.session.rollback()
        print("Ошибка сохранения таблицы countries в БД", f"<{e}>")


def save_city_db():
    """ Сохраняет данные из файла city.csv в таблицу в БД """
    from run import app
    from app.models import db, City
    db.session.close()
    try:
        df_city = pd.read_csv(f'{path_start_file}city.csv')
        with app.app_context():
            for row in df_city.itertuples(index=False):
                city = City(country_id=row.country,
                            region=row.region,
                            name=row.city,
                            link=row.link,
                            city_name=row.city_name,
                            city_num=row.city_num)
                db.session.add(city)
            db.session.commit()
        print("Таблица city успешно сохранена в БД")
    except Exception as e:
        db.session.rollback()
        print("Ошибка сохранения таблицы city в БД", f"<{e}>")


def save_data_in_db():
    save_countries_db()
    save_city_db()


if __name__ == "__main__":
    save_data_in_db()
