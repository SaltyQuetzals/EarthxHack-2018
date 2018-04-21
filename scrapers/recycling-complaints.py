import os
import sys

import django
import requests
from dateutil.parser import parse
from datetime import timedelta
from pprint import pprint

sys.path.append(
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '../server/')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from core.models import District, RecyclingComplaint

API_URL = 'https://www.dallasopendata.com/resource/mky5-34gc.json'


r = requests.get(API_URL)
complaints = r.json()

for complaint in complaints:
    district = District.objects.get(number=complaint['city_council_district'])
    created_date = parse(complaint['created_date'])
    closed_date = parse(complaint['closed_date'])
    if closed_date < created_date:
        created_date, closed_date = closed_date, created_date
    duration = closed_date - created_date
    print(duration.total_seconds()/3600)
    x_coord = complaint['x_coordinate']
    y_coord = complaint['y_coordinate']
    
