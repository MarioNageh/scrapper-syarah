import json
from django.http import HttpResponse
from datetime import datetime
from scrapper.models import Car


def cars_view(request):
    cars = Car.objects.all()
    min_len = 50
    cars_len = min(min_len, len(cars))
    cars = cars[:cars_len]

    car_list = []
    for car in cars:
        car_dict = {
            'name': car.name,
            'status': car.status,
            'price': car.price,
            'image_url': car.image_url,
            'currency': car.currency,
            'hash': car.hash,
            'scrapped_time': car.scrapped_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        car_list.append(car_dict)

    json_data = json.dumps(car_list)

    return HttpResponse(json_data, content_type='application/json')
