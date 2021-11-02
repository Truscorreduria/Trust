from django.conf import settings
import requests

headers = {'content-type': 'application/json',
           'Authorization': settings.TRAVEL_KEY}


def get_json(url, data=None):
    response = requests.get(url, headers=headers, params=data)
    if response.status_code == 200:
        json_data = response.json()
        if data['success'] == 1:
            return json_data['events']
        else:
            print(data, json_data)
    return []


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
