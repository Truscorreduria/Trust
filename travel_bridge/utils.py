from django.db import IntegrityError
from .api import *
from backend.models import *


def fetch_currencies():
    for coin in currencies():
        travel_coin, _ = CurrencyTravel.objects.get_or_create(iso=coin['value_iso'])
        travel_coin.name = coin['desc_small']
        travel_coin.save()


def fetch_category_plan():
    for category in category_plans():
        category_plan, _ = PlanCategoryTravel.objects.get_or_create(id=category['id_plan_categoria'])
        category_plan.name = category['name_plan']
        category_plan.save()


def fetch_territory():
    for region in regions():
        travel_territory, _ = TerritoryTravel.objects.get_or_create(id=region['id_territory'])
        travel_territory.name = region['desc_small']
        travel_territory.save()


def fetch_country():
    for country in countries():
        try:
            travel_country, _ = CountryTravel.objects.get_or_create(iso=country['iso_country'])
            travel_country.name = country['description']
            travel_country.save()
        except IntegrityError:
            print(country)


def fetch_city():
    for country in CountryTravel.objects.all():
        for city in cities(country.iso):
            try:
                travel_city, _ = CityTravel.objects.get_or_create(iso=city['iso_city'],
                                                                  country=country)
                travel_city.name = city['cities_description']
                travel_city.state = city['states_description']
                travel_city.save()
            except IntegrityError:
                print(city)


def fetch_plan():
    for plan in plans():
        travel_plan, _ = PlanTravel.objects.get_or_create(id=plan['plan_id'])
        travel_plan.title = plan['titulo']
        travel_plan.description = plan['description']
        travel_plan.languaje = plan['language_id']
        travel_plan.plan_category_id = plan['id_plan_categoria']
        travel_plan.num_pas = plan['num_pas']
        travel_plan.min_tiempo = plan['min_tiempo']
        travel_plan.max_tiempo = plan['max_tiempo']
        travel_plan.min_age = plan['min_age']
        travel_plan.max_age = plan['max_age']
        travel_plan.normal_age = plan['normal_age']
        travel_plan.plan_local = plan['plan_local']
        travel_plan.modo_plan = plan['modo_plan']
        travel_plan.combo = plan['combo']
        travel_plan.is_active = True
        travel_plan.save()


def fetch_benefit():
    for plan in PlanTravel.objects.all():
        for city in cities(plan.iso):
            try:
                travel_benefit, _ = BenefitTravel.objects.get_or_create(iso=city['id_benefit'])
                travel_benefit.plan = plan
                travel_benefit.name = city['name']
                travel_benefit.valor_eng = city['valor_eng']
                travel_benefit.valor_spa = city['valor_spa']
                travel_benefit.extended_info = city['extended_info']
                travel_benefit.save()
            except IntegrityError:
                print(city)
