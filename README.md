# Waypoint

A trail-finder and trip-planner, built from an object-oriented Python engine
into a Django web application. Term project for CCGC-5003.

## Project layout
- waypoint_core/ : pure-Python domain engine (Distance, Trail hierarchy, Itinerary).
- trails/ : Django app (models, views, admin, tests, templates wiring).
- waypoint/ : Django project settings, urls, wsgi/asgi.
- templates/ : base layout, partials, and page templates.
- static/ : stylesheet.
- manage.py : Django management entry point.

## Requirements
- Python 3.14
- Django 4.2

## Setup and run
1. python -m venv env
2. source env/Scripts/activate    (Windows Git Bash)
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py shell -c "from trails.models import Park, Trail; from decimal import Decimal; g=Park.objects.create(name='Gatineau Park', region='Quebec'); a=Park.objects.create(name='Algonquin Park', region='Ontario'); [Trail.objects.create(name=n, distance_km=Decimal(d), elevation_gain=e, difficulty=f, is_open=o, park=p) for n,d,e,f,o,p in [('River Loop','8.40',200,'easy',True,g),('Long Ridge','30.15',1500,'hard',True,a),('Sprint Path','6.00',100,'moderate',False,g),('Summit Chase','12.75',900,'expert',True,a),('Creek Walk','3.20',50,'easy',True,g),('Canyon Edge','18.90',1100,'expert',True,a)]]"
6. python manage.py runserver

Then open http://127.0.0.1:8000/ and http://127.0.0.1:8000/catalog/

## Pages
- / : home
- /catalog/ : open trails, ordered by distance, each showing its park
- /park/<id>/ : trails belonging to one park
- /report/ : CSRF-protected trail report form
- /search/ : query search
- /admin/ : Django admin (create a superuser first)

## Tests
Run: python manage.py test
Four tests cover the open-trails query, a 404 case, and domain rules from the engine.

## MVT note
Django follows the Model-View-Template pattern: models define data, views hold
request logic, and templates render the response.

## Screenshots
See the catalog and admin screenshots attached in the final pull request.

## Note on environment
The Django 4.2 admin add/change form and error-page rendering hit a known
Python 3.14 template incompatibility. Application pages, the ORM, and the test
suite all work; sample data can be seeded via the shell command in step 5.

## AI assistance
AI assistance was used for learning and debugging, disclosed per the course
integrity policy. All submitted code is understood by the author.
