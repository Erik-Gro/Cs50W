from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:blogName>", views.showWikiBlog, name="wikiBlog"),
    path("search/", views.search, name="search"),
    path("error/<str:err>", views.errorPage, name="failure"),
    path("createpage/",views.createPage,name="newPage"),
    path("smth/",views.smth,name="redirect"),
    path("edit/",views.edit,name="edit"),
    path("save/",views.save,name="save"),
]
