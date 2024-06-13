import asyncio
import json

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from bson.son import SON


class Database():
    # асинхронное подключение к MONGODB
    def __init__(self):
        client = AsyncIOMotorClient('localhost', 27017)
        db = client['sampleDB']
        self.collection = db['sample_collection']

    def generate_time_intervals(self, dt_from, dt_upto, group_type):
        current = dt_from
        intervals = []

        if group_type == 'hour':
            while current <= dt_upto:
                intervals.append(current)
                current += timedelta(hours=1)
        elif group_type == 'day':
            while current <= dt_upto:
                intervals.append(current)
                current += timedelta(days=1)
        elif group_type == 'month':
            while current <= dt_upto:
                intervals.append(current)
                if current.month == 12:
                    current = datetime(current.year + 1, 1, 1)
                else:
                    current = datetime(current.year, current.month + 1, 1)
        else:
            raise ValueError("Неподходящий тип агрегации")

        return intervals

    async def aggregate_salaries(self, dt_from, dt_upto, group_type):
        # преобразовываем строковые даты к datetime
        dt_from = datetime.fromisoformat(dt_from)
        dt_upto = datetime.fromisoformat(dt_upto)

        print(f"Агрегируем от {dt_from} до {dt_upto} по {group_type}")

        # устанавливаем группу агрегации по времени
        if group_type == 'hour':
            group_id = {
                'year': {'$year': '$dt'},
                'month': {'$month': '$dt'},
                'day': {'$dayOfMonth': '$dt'},
                'hour': {'$hour': '$dt'}
            }
            date_format = "%Y-%m-%dT%H:00:00"
        elif group_type == 'day':
            group_id = {
                'year': {'$year': '$dt'},
                'month': {'$month': '$dt'},
                'day': {'$dayOfMonth': '$dt'}
            }
            date_format = "%Y-%m-%dT00:00:00"
        elif group_type == 'month':
            group_id = {
                'year': {'$year': '$dt'},
                'month': {'$month': '$dt'}
            }
            date_format = "%Y-%m-01T00:00:00"
        else:
            raise ValueError("Неподходящий тип агрегации")

        # запрос агрегации
        pipeline = [
            {'$match': {'dt': {'$gte': dt_from, '$lte': dt_upto}}},
            {'$group': {
                '_id': group_id,
                'total_amount': {'$sum': '$value'}
            }},
            {'$sort': SON([('_id.year', 1), ('_id.month', 1), ('_id.day', 1), ('_id.hour', 1)])}
        ]

        results = []
        async for result in self.collection.aggregate(pipeline):
            results.append(result)

        # список всех временных интервалов
        intervals = self.generate_time_intervals(dt_from, dt_upto, group_type)

        # преобразуем результаты агрегации в словарь
        result_dict = {}
        for result in results:
            year = result['_id']['year']
            month = result['_id'].get('month', 1)
            day = result['_id'].get('day', 1)
            hour = result['_id'].get('hour', 0)

            key = datetime(year, month, day, hour).strftime(date_format)
            result_dict[key] = result['total_amount']

        dataset = []
        labels = []

        # заполняем интервалы, где нет данных
        for interval in intervals:
            label = interval.strftime(date_format)
            labels.append(label)
            dataset.append(result_dict.get(label, 0))

        print(f"dataset: {dataset}")
        print(f"labels: {labels}")

        return json.dumps({"dataset": dataset, "labels": labels})
