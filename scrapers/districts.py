import json
import sys
import os
import django
from pprint import pprint

sys.path.append(
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '../server/')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from core.models import District

features = json.load(open('./scrapers/Councils.json', 'r'))['features']
for feature in features:
    properties = feature['properties']
    number = int(properties['DISTRICT'])
    area = float(properties['SHAPE_Area'])
    district = District(number=number, area=area)
    district.save()