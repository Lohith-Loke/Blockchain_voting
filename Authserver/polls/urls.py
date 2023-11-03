from django.urls import path

from . import views

urlpatterns = [
    path("", views.all_list, name="index"),
    path("post/", views.genarte, name="index"),
]