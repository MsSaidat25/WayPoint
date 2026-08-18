# Waypoint

A trail-finder and trip-planner, built from an object-oriented Python engine
into a Django web app.

## Project layout
- waypoint_core/ : pure-Python domain engine (Distance, Trail hierarchy, Itinerary).
- waypoint/ : Django project (settings, urls, wsgi/asgi).
- manage.py : Django management entry point.

## Setup and run
1. python -m venv env
2. source env/Scripts/activate   (Windows Git Bash)
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py runserver

Then open http://127.0.0.1:8000/

## MVT note
Django follows the Model-View-Template pattern: models define data, views hold
request logic, and templates render the response.
