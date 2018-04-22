import json
import os
import sys
from pprint import pprint
from django.db import transaction

import django

sys.path.append(
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '../server/')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from core.models import District

@transaction.atomic
def collect():
    features = json.load(open('./scrapers/Councils.json', 'r'))['features']
    for feature in features:
        properties = feature['properties']
        number = int(properties['DISTRICT'])
        area = float(properties['SHAPE_Area'])
        population = int(properties['POPULATION'])
        district = District(number=number, area=area, population=population)
        district.save()

collect()