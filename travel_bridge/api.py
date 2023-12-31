from json import JSONDecodeError
from django.conf import settings
import requests


headers = {'content-type': 'application/json',
           'Authorization': settings.TRAVEL_KEY}


def get_json(url, data=None):
    response = requests.get(url, headers=headers, params=data)
    if response.status_code == 200:
        json_data = response.json()
        if json_data['success'] == 1:
            return json_data['events']
        else:
            print(data, json_data)
    return []


def post_data(url, data):
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        try:
            json_response = response.json()
            if not ('message' in json_response):
                try:
                    json_response['message'] = json_response['Message']
                except KeyError:
                    pass
            else:
                if isinstance(json_response['message'], dict):
                    json_response['message'] = json_response['message']['Notes']
            return json_response
        except JSONDecodeError:
            return {'success': '0', 'message': response.text}
    return {'success': '0', 'message': response.text}


def currencies():
    return get_json(f'{settings.TRAVEL_URL}/api/currencies')


def regions():
    return get_json(f'{settings.TRAVEL_URL}/api/regions')


def countries():
    return get_json(f'{settings.TRAVEL_URL}/api/countries')


def cities(iso_country):
    return get_json(f'{settings.TRAVEL_URL}/api/country_cities',
                    data={
                        'iso_country': iso_country
                    })


def plans():
    return get_json(f'{settings.TRAVEL_URL}/api/plans')


def category_plans():
    return get_json(f'{settings.TRAVEL_URL}/api/category_plans')


def coverages(id_play):
    return get_json(f'{settings.TRAVEL_URL}/api/coverages',
                    data={
                        'idPlan': id_play
                    })


def price_plan_age(data):
    return post_data(f'{settings.TRAVEL_URL}/api/price_plan_age', data)


def create_order(data):
    return post_data(f'{settings.TRAVEL_URL}/api/generate_order', data)
