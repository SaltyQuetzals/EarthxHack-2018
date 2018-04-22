# EcoPulse
For EarthxHack 2018: https://devpost.com/software/ecopulse

![Screencap of demo](https://raw.githubusercontent.com/SaltyQuetzals/EarthxHack-2018/master/screencap.gif)

# Prerequisites
* Install python-virtualenv
* Add API_KEY.txt to the scrapers/ folder with a [Google Maps API key](https://developers.google.com/maps/documentation/javascript/get-api-key)

## Setup
```
virtualenv env
source env/bin/activate
pip install djangorestframework markdown coreapi django beautifulsoup4 matplotlib tqdm
cd server
python manage.py makemigrations core
python manage.py migrate
python manage.py migrate --run-syncdb
cd ..
python scrapers/districts.py
python scrapers/city-council.py
python scrapers/garbage-complaints.py
python scrapers/recycling-complaints.py
```

## Startup
1. Run `python server/manage.py runserver`
1. Open [this page in your browser](http://localhost:8000/static/index.html)

## Todo
1. Proper checks for search returning out of district results
