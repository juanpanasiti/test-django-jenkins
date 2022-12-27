from django.urls import path

from purchases import views

urlpatterns = [
    path("", views.index, name="purchases-index"),
]
