from django.shortcuts import render


def home(request):
    # greet through a context variable (WP-402)
    context = {"greeting": "Welcome to Waypoint"}
    return render(request, "home.html", context)


def report(request):
    # GET shows a blank form; POST greets the reporter by name (WP-403)
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        trail = request.POST.get("trail", "")
        note = request.POST.get("note", "")
        context = {"name": name, "trail": trail, "note": note}
        return render(request, "thanks.html", context)
    return render(request, "report.html", {})


def search(request):
    # safely read the query string, default to empty (WP-404)
    q = request.GET.get("q", "")
    return render(request, "search.html", {"q": q})


def catalog(request):
    # data-driven catalog; edit these dicts to re-badge the page (WP-503)
    trails = [
        {"name": "River Loop", "distance": 8.4, "elevation": 200, "difficulty": "easy", "is_open": True},
        {"name": "Long Ridge", "distance": 30.15, "elevation": 1500, "difficulty": "hard", "is_open": True},
        {"name": "Sprint Path", "distance": 6.0, "elevation": 100, "difficulty": "moderate", "is_open": False},
        {"name": "Summit Chase", "distance": 12.75, "elevation": 900, "difficulty": "expert", "is_open": True},
        {"name": "Creek Walk", "distance": 3.2, "elevation": 50, "difficulty": "easy", "is_open": True},
        {"name": "Canyon Edge", "distance": 18.9, "elevation": 1100, "difficulty": "expert", "is_open": False},
    ]
    return render(request, "catalog.html", {"trails": trails})
