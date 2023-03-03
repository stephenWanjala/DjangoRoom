from django.urls import path

from . import views

urlpatterns = [
    path(route="", view=views.home, name="home"),
    path("room/", views.room, name="room")
]