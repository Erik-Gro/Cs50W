
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name="newPost"),
    path("allPosts/<str:page>", views.allPosts, name="allPosts"),
    path("Change/<str:page>", views.Change, name="Change"),
    path("Like/<str:page>", views.Like, name="Like"),
    path("Follow/<str:id>", views.Follow, name="Follow"),
    path("Profile/<str:id>/<str:page>/", views.Profile, name="Profile"),
    path("Followposts/<str:page>", views.Followposts, name="Followposts"),
    # path("test/<str:page>", views.test, name="test"),
]