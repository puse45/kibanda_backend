from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()


def index(request):
    context_data = {
        "title": "Kibanda Backend API ",
        "heading": "Kibanda Backend API v0.0.1",
    }
    return render(request, "index.html", context=context_data)


def about(request):
    context_data = {"title": "About Kibanda API"}
    return render(request, "about.html", context=context_data)


def releases(request):
    context_data = {"title": "Release notes"}
    return render(request, "releases.html", context=context_data)


def handler404(request, exception):
    return render(request, "errors/404.html", context={}, status=404)


def handler500(request):
    return render(request, "errors/500.html", context={}, status=500)
