from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("allCategories", views.allCategories, name="allCategories"),
    path("category/<str:ct>", views.categorylist, name="categorylist"),
    path("listing/<str:item>", views.showListing, name="showListing"),
    path("Watchlist", views.showWatchlist, name="showWatchlist"),
    path("addToWatchlist/<str:id>", views.addToWatchlist, name="addToWatchlist"),
    path("removeFromWatchlist/<str:id>", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("bid/<str:t>", views.bid, name="bid"),
    path("comment/<str:t>", views.comment, name="comment"),
    path("closeauc/<str:t>", views.closeauc, name="closeauc"),
]