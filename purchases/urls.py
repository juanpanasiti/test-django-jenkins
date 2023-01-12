from django.urls import path

from purchases import views

urlpatterns = [
    path("", views.index, name="purchases-index"),
    path(
        "credit-cards/<int:cc_id>",
        views.show_credit_card_by_id,
        name="show-credit-card",
    ),
    path("new", views.new_credit_card, name="credit-card-form"),
]
