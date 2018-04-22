import os
import sys
from datetime import timedelta
from pprint import pprint
from urllib.parse import quote
from tqdm import tqdm

import django
from django.db import transaction
import matplotlib.pyplot as plt
import requests
from dateutil.parser import parse

from common_functions import calculate_score

sys.path.append(
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '../server/')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from core.models import District, GarbageComplaint

API_KEYS = open('./scrapers/API_KEYS.txt', 'r').read().split('\n')


@transaction.atomic
def collect(i):
    API_URL = 'https://www.dallasopendata.com/resource/dc4g-i2n9.json?$limit=10000&$offset=%s' % (
        i * 10000)
    current_key = 0
    r = requests.get(API_URL)
    r.raise_for_status()
    complaints = r.json()
    scores = []
    for complaint in tqdm(complaints):
        if 'config_location_value' not in complaint:
            continue
        district = District.objects.get(
            number=complaint['config_location_value'])

        created_date = parse(complaint['created_date'])
        closed_date = parse(complaint['status_date'])
        if closed_date < created_date:
            created_date, closed_date = closed_date, created_date
        longitude = latitude = None
        if 'lat_long_location' in complaint:
            latitude, longitude = complaint['lat_long_location']['coordinates']
        else:
            GOOGLE_API_KEY = API_KEYS[current_key]
            address = None
            if 'lat_long_location_address' not in complaint:
                address = complaint['address']
            else:
                address = complaint['lat_long_location_address']
            GOOGLE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (
                address, GOOGLE_API_KEY)
            r = requests.get(GOOGLE_URL)
            r.raise_for_status()
            if len(r.json()['results']) > 0:
                geocoded_json = r.json()['results'][0]
                latitude, longitude = geocoded_json['geometry']['location'][
                    'lat'], geocoded_json['geometry']['location']['lng']
            else:
                print(
                    "Your Google Maps API key probably became rate limited, stopping...")
                current_key += 1
                continue
        score = calculate_score(created_date, closed_date,
                                district.area, district.population)
        if score > 10:
            continue
        scores.append(score)
        c = GarbageComplaint(created_date=created_date, closed_date=closed_date,
                             district=district, latitude=latitude, longitude=longitude, score=score)
        c.save()


for i in range(4):
    collect(i)
