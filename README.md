# EarthxHack Project Untitled

# Prerequisites
* Install python-virtualenv
* Add API_KEY.txt to the scrapers/ folder

## Setup
```
virtualenv env
source env/bin/activate
pip install djangorestframework markdown coreapi django beautifulsoup4 matplotlib
cd server
python manage.py makemigrations core
python manage.py migrate
python manage.py migrate --run-syncdb
cd ..
python scrapers/districts.py
python scrapers/city-council.py
python scrapers/*-complaints.py
```

## Startup
1. `python server/manage.py runserver`
1. Open [http://localhost:8000](http://localhost:8000)

## Todo
1. Remove statistics from garbage
