import os
import sys
from datetime import timedelta
from pprint import pprint
from urllib.parse import quote

import django
import requests
from dateutil.parser import parse
from django.db import transaction
from tqdm import tqdm

from common_functions import calculate_score

sys.path.append(
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '../server/')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from core.models import District, RecyclingComplaint

API_KEYS = open('./scrapers/API_KEYS.txt', 'r').read().split('\n')


@transaction.atomic
def collect(i):
    API_URL = 'https://www.dallasopendata.com/resource/mky5-34gc.json?$limit=10000&$offset=%s' % (
        i * 10000)
    current_key = 0
    r = requests.get(API_URL)
    complaints = r.json()

    for complaint in tqdm(complaints):
        if 'city_council_district' not in complaint:
            continue

        district = District.objects.get(
            number=complaint['city_council_district'])

        created_date = parse(complaint['created_date'])
        closed_date = parse(complaint['closed_date'])
        if closed_date < created_date:
            created_date, closed_date = closed_date, created_date
        longitude = latitude = None
        if 'lat_long_location' in complaint:
            latitude, longitude = complaint['lat_long_location']['coordinates']
        else:
            GOOGLE_API_KEY = API_KEYS[current_key]
            GOOGLE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (
                complaint['lat_long_location_address'], GOOGLE_API_KEY)
            r = requests.get(GOOGLE_URL)
            if len(r.json()['results']) > 0:
                geocoded_json = r.json()['results'][0]
                latitude, longitude = geocoded_json['geometry']['location'][
                    'lat'], geocoded_json['geometry']['location']['lng']
            else:
                print(
                    "Your Google Maps API key probably became rate limited, stopping...")
                current_key += 1
                break
        score = calculate_score(created_date, closed_date,
                                district.area, district.population)
        if score > 10:
            continue
        c = RecyclingComplaint(created_date=created_date, closed_date=closed_date,
                               district=district, latitude=latitude, longitude=longitude, score=score)
        c.save()


for i in range(4):
    collect(i)
