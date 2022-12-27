from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    dict_params = {
        "nbar": "home",
    }
    return render(request, "index.html", dict_params)
