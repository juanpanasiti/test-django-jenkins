from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from .models import CreditCard
from .forms import CreditCardForm

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:

    dict_params = {
        "nbar": "home",
        "credit_cards": CreditCard.objects.all(),
    }
    return render(request, "index.html", dict_params)


def show_credit_card_by_id(request: HttpRequest, cc_id: int) -> HttpResponse:
    credit_card = CreditCard.objects.get(id=cc_id)
    dict_params = {
        "credit_card": credit_card,
        "purchases": credit_card.purchases,
    }
    return render(request, "show_credit_card.html", dict_params)


def new_credit_card(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CreditCardForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "credit_card_form.html",
                {
                    "error": "Algo malió sal con el formulario.",
                    "form": form,
                },
            )

        new_cc = CreditCard(**form.cleaned_data)
        new_cc.save()
        return redirect("purchases-index")

    else:
        return render(request, "credit_card_form.html", {"form": CreditCardForm()})
