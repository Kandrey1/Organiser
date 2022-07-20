from flask import request, jsonify
from flask_restful import Resource
from ..weather.utils import CheckInputCity, CustomErrorNotDb,\
                            FutureTemperature, ArchiveTemperatureMonth
from ..models import TemperatureSchema


class RequestGetFutureCity(Resource):
    def get(self, city_n):
        try:
            cities = CheckInputCity().get_info_city(city_n)
            temp = {}
            for city in cities:
                t = FutureTemperature().get(city_id=city.id)
                name = f"{city.name} - {city.region}"
                temp[name] = t

        except ValueError as e:
            return {'message': 'Неправильный запрос'}
        except CustomErrorNotDb as e:
            return {'message': 'Такого города нет в БД'}
        return jsonify(temp)


class RequestGetArhive(Resource):
    def get(self):
        try:

            temp_schema = TemperatureSchema(many=True)

            data = request.get_json()
            archives = {}
            cities = CheckInputCity().get_info_city(data['city'])

            for city in cities:
                arch = ArchiveTemperatureMonth().get_archive(city_id=city.id,
                                                             year=data['year'],
                                                            month=data['month'])
                qq = temp_schema.dump(arch)
                name = f"{city.name} - {city.region}"
                archives[name] = qq

        except KeyError:
            return {'message': 'Ошибка. Неправильное имя параметра в данных'}
        return jsonify(archives)
