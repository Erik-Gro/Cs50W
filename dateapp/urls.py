from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("preference", views.preferences, name="preference"),
    path("dateapp", views.dateapp, name="dateapp"),
    path("loadmessagges/<str:id>", views.loadmessagges, name="loadmessagges"),
    path("loadmessagges/<str:id>", views.loadmessagges, name="loadmessagges"),
    path("loadcards/<str:id>", views.loadcards, name="loadcards"),
    path("add/<str:id>", views.add, name="add"),
    path("newmes/<str:id>", views.newmes, name="newmes"),
]
