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
