from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("report/", views.report, name="report"),
    path("search/", views.search, name="search"),
    path("catalog/", views.catalog, name="catalog"),
    path("park/<int:park_id>/", views.park_trails, name="park_trails"),
]
