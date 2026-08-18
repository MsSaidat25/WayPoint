from django.shortcuts import render
from .models import Trail


def home(request):
    context = {"greeting": "Welcome to Waypoint"}
    return render(request, "home.html", context)


def report(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        trail = request.POST.get("trail", "")
        note = request.POST.get("note", "")
        context = {"name": name, "trail": trail, "note": note}
        return render(request, "thanks.html", context)
    return render(request, "report.html", {})


def search(request):
    q = request.GET.get("q", "")
    return render(request, "search.html", {"q": q})


def catalog(request):
    # only open trails, ordered by distance, straight from the DB (WP-605)
    trails = Trail.objects.filter(is_open=True).order_by("distance_km")
    return render(request, "catalog.html", {"trails": trails})
